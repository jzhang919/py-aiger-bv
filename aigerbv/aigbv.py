from typing import Tuple, FrozenSet, NamedTuple

import aiger
import funcy as fn

from aigerbv import common


BV_MAP = FrozenSet[Tuple[str, Tuple[str]]]


def _blast(bvname2vals, name_map):
    if len(name_map) == 0:
        return dict()
    return fn.merge(*(dict(zip(names, bvname2vals[bvname]))
                      for bvname, names in name_map))


def _unblast(name2vals, name_map):
    def _collect(names):
        return tuple(name2vals[n] for n in names)

    return {bvname: _collect(names) for bvname, names in name_map}


class AIGBV(NamedTuple):
    aig: aiger.AIG
    input_map: BV_MAP
    output_map: BV_MAP
    latch_map: BV_MAP

    @property
    def inputs(self):
        return set(fn.pluck(0, self.input_map))

    @property
    def outputs(self):
        return set(fn.pluck(0, self.output_map))

    @property
    def latches(self):
        return set(fn.pluck(0, self.latch_map))

    def __getitem__(self, others):
        if not isinstance(others, tuple):
            return super().__getitem__(others)

        kind, relabels = others
        if kind not in {'i', 'o', 'l'}:
            raise NotImplementedError

        attr_name = {
            'i': 'input_map',
            'o': 'output_map',
            'l': 'latch_map',
        }.get(kind)

        attr_value = fn.walk_keys(lambda x: relabels.get(x, x),
                                  getattr(self, attr_name))
        return self._replace(**{attr_name: attr_value})

    def __rshift__(self, other):
        interface = self.outputs & other.inputs

        assert not self.latches & other.latches
        assert not (self.outputs - interface) & other.outputs

        # Relabel interface to match up.
        aig = self.aig
        if interface:
            imap, omap = dict(other.input_map), dict(self.output_map)
            relabels = fn.merge(*(
                dict(zip(omap[name], imap[name])) for name in interface
            ))
            aig = aig[('o', relabels)]

        # Create composed aigbv
        input_map2 = {kv for kv in other.input_map if kv[0] not in interface}
        output_map2 = {kv for kv in self.output_map if kv[0] not in interface}
        return AIGBV(
            aig=aig >> other.aig,
            input_map=self.input_map | input_map2,
            output_map=output_map2 | other.output_map,
            latch_map=self.latch_map | other.latch_map,
        )

    def __or__(self, other):
        assert not self.inputs & other.inputs
        assert not self.outputs & other.outputs
        assert not self.latches & other.latches

        return AIGBV(
            aig=self.aig | other.aig,
            input_map=self.input_map | other.input_map,
            output_map=self.output_map | other.output_map,
            latch_map=self.latch_map | other.latch_map)

    def __call__(self, inputs, latches=None):
        if latches is None:
            latches = dict()

        out_vals, latch_vals = self.aig(
            inputs=_blast(inputs, self.input_map),
            latches=_blast(latches, self.latch_map))
        outputs = _unblast(out_vals, self.output_map)
        latch_outs = _unblast(latch_vals, self.latch_map)
        return outputs, latch_outs

    def simulator(self, latches=None):
        inputs = yield
        while True:
            outputs, latches = self(inputs, latches)
            inputs = yield outputs, latches

    def simulate(self, input_seq, latches=None):
        sim = self.simulator()
        next(sim)
        return [sim.send(inputs) for inputs in input_seq]

    def write(self, path):
        self.aig.write(path)

    def feedback(self, inputs, outputs, initials=None, latches=None,
                 keep_outputs=False):
        if latches is None:
            latches = inputs

        idrop, imap = fn.lsplit(lambda x: x[0] in inputs, self.input_map)
        odrop, omap = fn.lsplit(lambda x: x[0] in outputs, self.output_map)

        wordlens = [len(vals) for _, vals in self.input_map]
        new_latches = [(n, common.named_indexes(k, n)) 
                       for k, n in zip(wordlens, latches)]

        if initials is not None:
            initials = fn.lcat([i]*k for k, i in zip(wordlens, initials))

        def get_names(key_vals):
            return fn.lcat(fn.pluck(1, key_vals))

        aig = self.aig.feedback(
            inputs=get_names(idrop),
            outputs=get_names(odrop),
            latches=get_names(new_latches),
            initials=initials,
            keep_outputs=keep_outputs,
        )

        imap, odrop, omap = map(frozenset, [imap, odrop, omap])
        return AIGBV(
            aig=aig,
            input_map=imap,
            output_map=omap | (odrop if keep_outputs else {}),
            latch_map=self.latch_map | set(new_latches),
        )

    def unroll(self, horizon, *, init=True, omit_latches=True):
        aig = self.aig.unroll(horizon, init=init, omit_latches=omit_latches)
        # TODO: generalize and apply to all maps.

        def extract_map(name_map, names):
            lookup_root = fn.merge(*(
                {v: k for v in vals} for k, vals in name_map)
            )
            return frozenset(fn.group_by(
                lambda x: lookup_root[x.split('##time_')[0]],
                names
            ).items())

        return AIGBV(
            aig=aig,
            input_map=extract_map(self.input_map, aig.inputs),
            output_map=extract_map(self.output_map, aig.outputs),
            latch_map=extract_map(self.latch_map, aig.latches),
        )


def _diagonal_map(keys, frozen=True):
    dmap = {k: (k,) for k in keys}
    return frozenset(dmap.items()) if frozen else dmap


def aig2aigbv(aig):
    return AIGBV(
        aig=aig,
        input_map=_diagonal_map(aig.inputs),
        output_map=_diagonal_map(aig.outputs),
        latch_map=_diagonal_map(aig.latches),
    )
