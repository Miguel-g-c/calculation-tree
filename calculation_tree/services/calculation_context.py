from __future__ import annotations
from typing import Any, Iterator
from calculation_tree.services.collections import (
    VariableCollection,
    DataSourceCollection,
    OperationCollection,
)
from calculation_tree.model import Node
from calculation_tree.model.node import TraverseCallback


class CalculationContext:
    data_sources: DataSourceCollection
    variables: VariableCollection
    operations: OperationCollection

    def __enter__(self) -> CalculationContext:
        self.data_sources = DataSourceCollection()
        self.variables = VariableCollection()
        self.operations = OperationCollection()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        pass

    def __repr__(self) -> str:
        if not self.final_result:
            return ""
        return self.final_result.render_tree()

    @property
    def nodes(self) -> Iterator[Node]:
        yield from self.data_sources
        yield from self.operations
        yield from self.variables

    @property
    def final_result(self) -> Node | None:
        if n := next(self.nodes, None):
            return n.final_result
        return None

    def traverse(self, callback: TraverseCallback, **kwargs: Any) -> None:
        if not self.final_result:
            return
        return self.final_result.traverse(callback, **kwargs)
