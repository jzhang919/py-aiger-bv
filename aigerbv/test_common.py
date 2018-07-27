from aigerbv import common

# additional imports for testing frammework
import hypothesis.strategies as st
from hypothesis import given


@given(st.integers(-4, 3))
def test_source(int_value):
    var = common.source(wordlen=4, value=int_value, name='x')
    assert common.decode_int(var({})[0]['x']) == int_value


@given(st.integers(-4, 3), st.integers(-4, 3))
def test_bitwise_and(a, b):
    circ = common.bitwise_and(4, left='a', right='b', output='out')
    val = circ({
        'a': common.encode_int(4, a),
        'b': common.encode_int(4, b),
    })[0]['out']
    assert common.decode_int(val) == a & b


@given(st.integers(-4, 3), st.integers(-4, 3))
def test_bitwise_or(a, b):
    circ = common.bitwise_or(4, left='a', right='b', output='out')
    val = circ({
        'a': common.encode_int(4, a),
        'b': common.encode_int(4, b),
    })[0]['out']
    assert common.decode_int(val) == a | b


@given(st.integers(-4, 3))
def test_bitwise_negate(a):
    circ = common.bitwise_negate(4, input='a', output='out')
    val = circ({'a': common.encode_int(4, a)})[0]['out']
    assert common.decode_int(val) == ~a


@given(st.integers(-4, 3))
def test_is_nonzero(a):
    circ = common.is_nonzero_gate(4, input='a', output='out')
    val = circ({'a': common.encode_int(4, a)})[0]['out']
    assert val[0] == (a != 0)


@given(st.integers(-4, 3))
def test_is_zero(a):
    circ = common.is_zero_gate(4, input='a', output='out')
    val = circ({'a': common.encode_int(4, a)})[0]['out']
    assert val[0] == (a == 0)

    
@given(st.integers(-4, 3), st.integers(-4, 3))
def test_neq(a, b):
    circ = common.neq_gate(4, left='a', right='b', output='out')
    val = circ({
        'a': common.encode_int(4, a),
        'b': common.encode_int(4, b),
    })[0]['out']
    assert val[0] == (a != b)


@given(st.integers(-4, 3), st.integers(-4, 3))
def test_eq(a, b):
    circ = common.eq_gate(4, left='a', right='b', output='out')
    val = circ({
        'a': common.encode_int(4, a),
        'b': common.encode_int(4, b),
    })[0]['out']
    assert val[0] == (a == b)


@given(st.integers(-4, 3))
def test_identity(a):
    circ = common.identity_gate(4, input='a', output='out')
    val = circ({'a': common.encode_int(4, a)})[0]['out']
    assert common.decode_int(val) == a


@given(st.integers(-4, 3))
def test_reverse(a):
    circ = common.reverse_gate(4, input='a', output='out')
    val = circ({'a': common.encode_int(4, a)})[0]['out']
    assert common.decode_int(val[::-1]) == a


@given(st.integers(-4, 3), st.integers(-4, 3))
def test_combine_gate(a, b):
    circ = common.combine_gate(4, 'a', 4, 'b', output='out')
    val = circ({
        'a': common.encode_int(4, a),
        'b': common.encode_int(4, b)
    })[0]['out']
    assert common.decode_int(val[:4]) == a
    assert common.decode_int(val[4:]) == b


@given(st.integers(-4, 3), st.integers(-4, 3))
def test_split_gate(a, b):
    circ = common.split_gate('input', 4, 'a', 4, 'b')
    val = circ({
        'input': common.encode_int(4, a) + common.encode_int(4, b),
    })[0]
    assert common.decode_int(val['a']) == a
    assert common.decode_int(val['b']) == b


@given(st.integers(-4, 3), st.integers(-4, 3))
def test_addition(a, b):
    circ = common.add_gate(4, left='a', right='b', output='out')
    val = circ({
        'a': common.encode_int(4, a),
        'b': common.encode_int(4, b),
    })[0]['out']
    assert common.decode_int(val) == a + b