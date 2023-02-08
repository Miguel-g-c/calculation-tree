from __future__ import annotations
import json
from typing import Any, Iterator
from calculation_tree.services.collections import (
    VariableCollection,
)
from calculation_tree.model import Node
from calculation_tree.model.node import TraverseCallback
from calculation_tree.services.mocks import (
    ConversionFactor,
    EmissionFactor,
    FakeRepository,
    PriceIndex,
    generate_conversion_factors,
    generate_emission_factors,
    generate_price_indices,
)


class CalculationContext:
    variables: VariableCollection
    emission_factors: FakeRepository[EmissionFactor]
    price_indices: FakeRepository[PriceIndex]
    conversion_factors: FakeRepository[ConversionFactor]

    def __enter__(self) -> CalculationContext:
        self.variables = VariableCollection()
        self.emission_factors = FakeRepository[EmissionFactor](
            generate_emission_factors()
        )
        self.price_indices = FakeRepository[PriceIndex](generate_price_indices())
        self.conversion_factors = FakeRepository[ConversionFactor](
            generate_conversion_factors()
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        pass

    def __repr__(self) -> str:
        if not self.final_result:
            return ""
        return self.final_result.render_tree()

    @property
    def nodes(self) -> Iterator[Node]:
        yield from self.variables
        yield from self.emission_factors.seen
        yield from self.price_indices.seen
        yield from self.conversion_factors.seen

    @property
    def final_result(self) -> Node | None:
        if n := next(self.nodes, None):
            return n.final_result
        return None

    def traverse(self, callback: TraverseCallback, **kwargs: Any) -> None:
        if not self.final_result:
            return
        return self.final_result.traverse(callback, **kwargs)

    def to_dict(self) -> dict[str, Any]:
        if not self.final_result:
            return {}
        return self.final_result.to_dict()

    def to_json(self) -> str:
        return json.dumps(self.to_dict())
