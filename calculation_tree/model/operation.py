from __future__ import annotations
from typing import Any, Protocol, TYPE_CHECKING
import uuid

from calculation_tree.model import Node

if TYPE_CHECKING:
    from calculation_tree.model import Variable


class OperationCallback(Protocol):
    __name__: str

    def __call__(self, *args: Variable, **kwarg: Any) -> Variable:
        ...


class Operation(Node):
    def __init__(
        self,
        name: str,
        parents: list[Variable] | None = None,
        child: Variable | None = None,
        id_: uuid.UUID | None = None,
    ) -> None:
        super().__init__(name, parents, child, id_)

    def __str__(self) -> str:
        return f"{self.name}({', '.join([str(p) for p in self.parents])})"

    @classmethod
    def from_function(
        cls, function: OperationCallback, parents: list[Variable], **kwargs: Any
    ) -> Operation:
        child = function(*parents, **kwargs)
        operation = cls(
            name=function.__name__,
            parents=parents,
            child=child,
        )
        if not child.is_child_of(operation):
            child._parents.append(operation)
        for parent in parents:
            parent._child = operation
        return operation
