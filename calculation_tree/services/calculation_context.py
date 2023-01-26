from __future__ import annotations
from typing import Iterator
from calculation_tree.services.collections import (
    VariableCollection,
    DataSourceCollection,
    OperationCollection,
)
from calculation_tree.model import Node


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

    @property
    def nodes(self) -> Iterator[Node]:
        yield from self.variables
        yield from self.operations
        yield from self.data_sources

    @property
    def final_result(self) -> Node | None:
        n = next(self.nodes, None)
        if n:
            return n.final_result
        return None
