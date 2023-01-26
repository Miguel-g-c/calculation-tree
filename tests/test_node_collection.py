from calculation_tree.model import Node, Variable
from calculation_tree.services.collections import (
    NodeCollection,
    VariableCollection,
    DataSourceCollection,
    OperationCollection,
)


def test_add_node():
    node1 = Node("node1")
    node2 = Node("node2")
    nodes = NodeCollection()
    nodes.add(node1)
    nodes.add(node2)
    assert nodes == {node1, node2}


def test_contains_node():
    node1 = Node("node1")
    node2 = Node("node2")
    nodes = NodeCollection()
    nodes.add(node1)
    assert node1 in nodes
    assert node2 not in nodes


def test_remove_node():
    node1 = Node("node1")
    node2 = Node("node2")
    nodes = NodeCollection()
    nodes.add(node1)
    nodes.add(node2)
    nodes.remove(node1)
    assert nodes == {node2}


def test_iterate_over_nodes():
    node1 = Node("node1")
    nodes = NodeCollection()
    nodes.add(node1)
    assert next(n for n in nodes) == node1


def test_create_variable():
    variables = VariableCollection()
    var = variables.create("var", 1)
    assert var in variables


def test_create_data_source():
    data_sources = DataSourceCollection()
    ds = data_sources.create("ds", "description", 2021)
    assert ds in data_sources


def test_create_operation():
    operations = OperationCollection()
    op = operations.create("op")
    assert op in operations


def test_create_operation_with_callback():
    def add(x: Variable, y: Variable) -> Variable:
        return Variable("x + y", x.value + y.value)

    x = Variable("x", 1)
    y = Variable("y", 2)
    operations = OperationCollection()
    op = operations.from_function(add, parents=[x, y])
    assert op in operations
