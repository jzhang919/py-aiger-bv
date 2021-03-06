from aigerbv.expr import atom, ite
from aigerbv import common

# additional imports for testing frammework
import hypothesis.strategies as st
from hypothesis import given


@given(st.integers(0, 7), st.integers(0, 3))
def test_srl_unsigned(a, b):
    expr = atom(4, a) >> b
    assert common.decode_int(expr(), signed=False) == a >> b


@given(st.integers(-8, 7), st.integers(0, 3))
def test_srl_signed(a, b):
    expr = atom(4, a) >> b
    assert common.decode_int(expr()) == a >> b


@given(st.integers(0, 7), st.integers(0, 3))
def test_sll(a, b):
    wordlen = 4
    expr = atom(wordlen, a, signed=False) << b
    mask = (1 << wordlen) - 1
    assert bin(common.decode_int(expr(), signed=False)) == bin((a << b) & mask)


@given(st.integers(0, 7), st.integers(0, 7))
def test_expr_unsigned_lt_literal(a, b):
    expr = atom(4, a, signed=False) < b
    assert expr()[0] == (a < b)


@given(st.integers(0, 7), st.integers(0, 7))
def test_expr_unsigned_gt_literal(a, b):
    expr = atom(4, a, signed=False) > b
    assert expr()[0] == (a > b)


@given(st.integers(0, 7), st.integers(0, 7))
def test_expr_unsigned_ge_literal(a, b):
    expr = atom(4, a, signed=False) >= b
    assert expr()[0] == (a >= b)


@given(st.integers(0, 7), st.integers(0, 7))
def test_expr_unsigned_le_literal(a, b):
    expr = atom(4, a, signed=False) <= b
    assert expr()[0] == (a <= b)


@given(st.integers(-7, 7), st.integers(0, 7))
def test_expr_signed_lt_literal(a, b):
    expr = atom(4, a, signed=True) < b
    assert expr()[0] == (a < b)


@given(st.integers(-7, 7), st.integers(0, 7))
def test_expr_signed_gt_literal(a, b):
    expr = atom(4, a, signed=True) > b
    assert expr()[0] == (a > b)


@given(st.integers(-7, 7), st.integers(0, 7))
def test_expr_signed_ge_literal(a, b):
    expr = atom(4, a, signed=True) >= b
    assert expr()[0] == (a >= b)


@given(st.integers(-7, 7), st.integers(0, 7))
def test_expr_signed_le_literal(a, b):
    expr = atom(4, a, signed=True) <= b
    assert expr()[0] == (a <= b)


@given(st.integers(-4, 3), st.integers(-4, 3))
def test_expr_bitwise_and(a, b):
    expr = atom(4, a) & atom(4, b)
    assert common.decode_int(expr()) == a & b


@given(st.integers(-4, 3))
def test_expr_bitwise_and2(a):
    expr = atom(4, a) & atom(4, a)
    assert common.decode_int(expr()) == a


@given(st.integers(-4, 3), st.integers(-4, 3))
def test_expr_bitwise_or(a, b):
    expr = atom(4, a) | atom(4, b)
    assert common.decode_int(expr()) == a | b


@given(st.integers(-4, 3), st.integers(-4, 3))
def test_expr_bitwise_xor(a, b):
    expr = atom(4, a) ^ atom(4, b)
    assert common.decode_int(expr()) == a ^ b


@given(st.integers(-4, 3))
def test_expr_bitwise_invert(a):
    expr = ~atom(4, a)
    assert common.decode_int(expr()) == ~a


@given(st.integers(-4, 3), st.integers(-4, 3))
def test_expr_eq(a, b):
    expr = atom(4, a) == atom(4, b)
    assert expr()[0] == (a == b)


@given(st.integers(-4, 3), st.integers(-4, 3))
def test_expr_ne(a, b):
    expr = atom(4, a) != atom(4, b)
    assert expr()[0] == (a != b)


@given(st.integers(-4, 3), st.integers(-4, 3))
def test_expr_add(a, b):
    expr = atom(4, a) + atom(4, b)
    assert common.decode_int(expr()) == a + b


@given(st.integers(-4, 3), st.integers(-4, 3))
def test_expr_sub(a, b):
    expr = atom(4, a) - atom(4, b)
    assert common.decode_int(expr()) == a - b


@given(st.integers(-4, 3), st.integers(-4, 3))
def test_expr_le(a, b):
    expr = atom(4, a) <= atom(4, b)
    assert expr()[0] == (a <= b)


@given(st.integers(-4, 3), st.integers(-4, 3))
def test_expr_lt(a, b):
    expr = atom(4, a) < atom(4, b)
    assert expr()[0] == (a < b)


@given(st.integers(-4, 3), st.integers(-4, 3))
def test_expr_ge(a, b):
    expr = atom(4, a) >= atom(4, b)
    assert expr()[0] == (a >= b)


@given(st.integers(-4, 3), st.integers(-4, 3))
def test_expr_gt(a, b):
    expr = atom(4, a) > atom(4, b)
    assert expr()[0] == (a > b)


@given(st.integers(0, 7), st.integers(0, 7))
def test_expr_unsigned_le(a, b):
    expr = atom(4, a, signed=False) <= atom(4, b, signed=False)
    assert expr()[0] == (a <= b)


@given(st.integers(0, 7), st.integers(0, 7))
def test_expr_unsigned_lt(a, b):
    expr = atom(4, a, signed=False) < atom(4, b, signed=False)
    assert expr()[0] == (a < b)


@given(st.integers(0, 7), st.integers(0, 7))
def test_expr_unsigned_gt(a, b):
    expr = atom(4, a, signed=False) > atom(4, b, signed=False)
    assert expr()[0] == (a > b)


@given(st.integers(0, 7), st.integers(0, 7))
def test_expr_unsigned_ge(a, b):
    expr = atom(4, a, signed=False) >= atom(4, b, signed=False)
    assert expr()[0] == (a >= b)


@given(st.integers(-4, 3))
def test_expr_neg(a):
    expr = -atom(4, a)
    assert common.decode_int(expr()) == -a


@given(st.integers(-4, 3))
def test_expr_abs(a):
    expr = abs(atom(4, a))
    assert common.decode_int(expr()) == abs(a)


@given(st.integers(-4, 3))
def test_expr_getitem(a):
    expr = atom(4, a)
    for i in range(4):
        assert common.decode_int(expr[i](), signed=False) == (a >> i) & 1


@given(st.integers(-4, 3), st.integers(-4, 3))
def test_expr_concat(a, b):
    expr1, expr2 = atom(4, a), atom(4, b)
    expr3 = expr1.concat(expr2)
    assert expr3.size == expr1.size + expr2.size
    assert expr3() == expr1() + expr2()


@given(st.booleans(), st.integers(1, 5))
def test_expr_repeat(a, b):
    expr = atom(1, a, signed=False)
    assert expr.repeat(b)() == b * expr()


@given(st.integers(-4, 3), st.integers(-4, 3))
def test_expr_dotprod_mod2(a, b):
    expr1, expr2 = atom(4, a), atom(4, b)
    expr3 = expr1 @ expr2
    val = sum([x * y for x, y in zip(expr1(), expr2())])
    assert expr3()[0] == bool(val % 2)


@given(st.booleans(), st.integers(-4, 3), st.integers(-4, 3))
def test_ite(test, a, b):
    _test, _a, _b = atom(1, test, signed=False), atom(4, a), atom(4, b)
    expr = ite(_test, _a, _b)
    val = common.decode_int(expr())
    assert val == (a if test else b)
