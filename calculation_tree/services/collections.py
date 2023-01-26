from collections.abc import MutableSet
from typing import Any, Generic, Iterator, TypeVar
import uuid

from calculation_tree.model import Node, DataSource, Variable, Operation
from calculation_tree.model.operation import OperationCallback
from calculation_tree.model.variable import NUMERIC


T = TypeVar("T", bound=Node)


class NodeCollection(MutableSet[T], Generic[T]):
    def __init__(self) -> None:
        self._nodes = set[T]()

    def __iter__(self) -> Iterator[T]:
        return iter(self._nodes)

    def __len__(self) -> int:
        return len(self._nodes)

    def __contains__(self, node: object) -> bool:
        return node in self._nodes

    def add(self, node: T) -> None:
        self._nodes.add(node)

    def discard(self, node: T) -> None:
        self._nodes.discard(node)


class VariableCollection(NodeCollection[Variable]):
    def create(
        self,
        name: str,
        value: NUMERIC,
        parents: list[Node] | None = None,
        child: Node | None = None,
        id_: uuid.UUID | None = None,
    ) -> Variable:
        var = Variable(name, value, parents, child, id_)
        self.add(var)
        return var


class DataSourceCollection(NodeCollection[DataSource]):
    def create(
        self,
        name: str,
        description: str | None = None,
        year: int | None = None,
        child: Variable | None = None,
        id_: uuid.UUID | None = None,
    ) -> DataSource:
        ds = DataSource(name, description, year, child, id_)
        self.add(ds)
        return ds


class OperationCollection(NodeCollection[Operation]):
    def create(
        self,
        name: str,
        parents: list[Variable] | None = None,
        child: Variable | None = None,
        id_: uuid.UUID | None = None,
    ) -> Operation:
        op = Operation(name, parents, child, id_)
        self.add(op)
        return op

    def from_function(
        self, function: OperationCallback, parents: list[Variable], **kwargs: Any
    ) -> Operation:
        op = Operation.from_function(function, parents, **kwargs)
        self.add(op)
        return op
