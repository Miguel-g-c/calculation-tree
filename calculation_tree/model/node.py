from __future__ import annotations
from typing import Any, Protocol, Sequence
import uuid


class TraverseCallback(Protocol):
    def __call__(self, node: Node, **kwarg: Any) -> None:
        ...


class Node:
    def __init__(
        self,
        name: str,
        parents: Sequence[Node] | None = None,
        child: Node | None = None,
        id_: uuid.UUID | None = None,
    ) -> None:
        self._id = str(id_) if id_ is not None else str(uuid.uuid4())
        self._name = name
        self._parents = list(parents) if parents is not None else []
        self._child = child

    def __repr__(self) -> str:
        class_name = type(self).__name__
        return f"{class_name}({self.name})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def parents(self) -> list[Node]:
        return self._parents

    @property
    def child(self) -> Node | None:
        return self._child

    @property
    def is_root(self) -> bool:
        return len(self.parents) == 0

    @property
    def is_leaf(self) -> bool:
        return self.child is None

    @property
    def roots(self) -> list[Node]:
        roots = set()
        if self.is_root:
            roots.add(self)
        for parent in self.parents:
            roots.update(parent.roots)
        return list(roots)

    @property
    def final_result(self) -> Node:
        if self.is_leaf:
            return self
        return self.child.final_result  # type: ignore

    def is_child_of(self, node: Node) -> bool:
        return node in self.parents

    def is_parent_of(self, node: Node) -> bool:
        return node == self.child

    def traverse(self, callback: TraverseCallback, **kwargs: Any) -> None:
        callback(self, **kwargs)
        for parent in self.parents:
            parent.traverse(callback, **kwargs)

    def render_tree(self, depth: int = 0, final: bool = False) -> str:
        tree = ""
        if depth > 0:
            tree += " " * 4 * (depth - 1) + "│   " + "\n"
            tree += " " * 4 * (depth - 1) + "├── " if not final else ""
            tree += " " * 4 * (depth - 1) + "└── " if final else ""
        tree += str(self) + "\n"
        for i, parent in enumerate(self.parents):
            tree += parent.render_tree(depth + 1, i == len(self.parents) - 1)
        return tree
