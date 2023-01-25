from decimal import Decimal
from calculation_tree.model import Variable, Operation


def test_variable_repr():
    variable = Variable("variable", 1.0)
    assert repr(variable) == "Variable(variable, 1.00)"


def test_variable_print():
    variable = Variable("variable", 1.0)
    assert str(variable) == "variable = 1.0"


def test_variable_value_with_float():
    variable = Variable("variable", 1.0)
    assert variable.value == 1.0


def test_variable_value_with_int():
    variable = Variable("variable", 1)
    assert variable.value == 1.0


def test_variable_value_with_decimal():
    variable = Variable("variable", Decimal("1.0"))
    assert variable.value == 1.0


def test_variable_int():
    variable = Variable("variable", 1.1)
    assert int(variable) == 1


def test_variable_float():
    variable = Variable("variable", 1.1)
    assert float(variable) == 1.1


def test_add_two_variables():
    x = Variable("x", 1.0)
    y = Variable("y", 2.0)
    z = x + y
    assert z.name == "x + y"
    assert z.value == 3.0
    assert type(z.parents[0]) == Operation
    assert z.parents[0].name == "add"
    assert z.parents[0].child == z


def test_sub_two_variables():
    x = Variable("x", 1.0)
    y = Variable("y", 2.0)
    z = x - y
    assert z.name == "x - y"
    assert z.value == -1.0
    assert type(z.parents[0]) == Operation
    assert z.parents[0].name == "sub"
    assert z.parents[0].child == z


def test_mul_two_variables():
    x = Variable("x", 1.0)
    y = Variable("y", 2.0)
    z = x * y
    assert z.name == "x * y"
    assert z.value == 2.0
    assert type(z.parents[0]) == Operation
    assert z.parents[0].name == "mul"
    assert z.parents[0].child == z


def test_true_div_two_variables():
    x = Variable("x", 1.0)
    y = Variable("y", 2.0)
    z = x / y
    assert z.name == "x / y"
    assert z.value == 0.5
    assert type(z.parents[0]) == Operation
    assert z.parents[0].name == "truediv"
    assert z.parents[0].child == z


def test_pow_two_variables():
    x = Variable("x", 1.0)
    y = Variable("y", 2.0)
    z = x**y
    assert z.name == "x ** y"
    assert z.value == 1.0
    assert type(z.parents[0]) == Operation
    assert z.parents[0].name == "pow"
    assert z.parents[0].child == z


def test_neg_variable():
    x = Variable("x", 1.0)
    y = -x
    assert y.name == "-x"
    assert y.value == -1.0
    assert type(y.parents[0]) == Operation
    assert y.parents[0].name == "neg"
    assert y.parents[0].child == y


def test_abs_variable():
    x = Variable("x", -1.0)
    y = abs(x)
    assert y.name == "abs(x)"
    assert y.value == 1.0
    assert type(y.parents[0]) == Operation
    assert y.parents[0].name == "abs"
    assert y.parents[0].child == y
