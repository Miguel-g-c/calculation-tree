from calculation_tree.model import Operation, Variable


def test_operation_print():
    operation = Operation("operation", parents=[Variable("x", 1), Variable("y", 2)])
    assert str(operation) == "operation(x = 1.0, y = 2.0)"


def test_from_function_constructor():
    def add(x: Variable, y: Variable) -> Variable:
        return Variable(f"{x.name} + {y.name}", x.value + y.value)

    x = Variable("x", 1)
    y = Variable("y", 2)
    operation = Operation.from_function(add, parents=[x, y])

    assert operation.name == "add"
    assert operation.parents == [x, y]
    assert operation.child is not None
    assert operation.child.name == "x + y"
    assert operation.child.value == 3.0


def test_from_function_kwars():
    def add(x: Variable, y: Variable, variable_name: str) -> Variable:
        return Variable(variable_name, x.value + y.value)

    x = Variable("x", 1)
    y = Variable("y", 2)
    operation = Operation.from_function(add, parents=[x, y], variable_name="testing")

    assert operation.child.name == "testing"
    assert operation.child.value == 3.0
