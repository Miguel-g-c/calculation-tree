from calculation_tree.model import Node


def test_node_repr():
    node = Node("node")
    assert repr(node) == "Node(node)"


def test_node_can_be_used_in_a_set():
    node1 = Node("node1")
    node2 = Node("node2")
    nodes = {node1, node2}
    nodes.add(node1)
    node3 = Node("node3")
    nodes.add(node3)
    assert nodes == {node1, node2, node3}


def test_node_parents():
    node1 = Node("node1")
    node2 = Node("node2")
    node3 = Node("node3", parents=[node1, node2])
    assert node3.parents == [node1, node2]


def test_node_is_child_of():
    node1 = Node("node1")
    node2 = Node("node2", parents=[node1])
    assert node2.is_child_of(node1)


def test_node_child():
    node1 = Node("node1")
    node2 = Node("node2", child=node1)
    assert node2.child == node1


def test_node_is_parent_of():
    node1 = Node("node1")
    node2 = Node("node2", child=node1)
    assert node2.is_parent_of(node1)


def test_node_is_root():
    node1 = Node("node1")
    node2 = Node("node2", parents=[node1])
    assert node1.is_root
    assert not node2.is_root


def test_node_is_leaf():
    node1 = Node("node1")
    node2 = Node("node2", child=node1)
    assert node1.is_leaf
    assert not node2.is_leaf


def test_node_roots():
    node1 = Node("node1")
    node2 = Node("node2")
    node3 = Node("node3", parents=[node1, node2])
    node4 = Node("node4", parents=[node3])
    assert set(node4.roots) == set([node1, node2])


def test_node_final_result():
    node1 = Node("node1")
    node2 = Node("node2", child=node1)
    node3 = Node("node3", child=node2)
    assert node3.final_result == node1
