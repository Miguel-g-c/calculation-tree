from typing import Generic, Iterable, TypeVar
import uuid

from calculation_tree.model import DataSource, Node, Variable
from calculation_tree.model.variable import NUMERIC


class MappedVariable(Variable):
    def __init__(
        self,
        normid: str,
        year: int,
        region: str,
        name: str,
        value: NUMERIC,
        parents: list[Node] | None = None,
        child: Node | None = None,
        id_: uuid.UUID | None = None,
    ) -> None:
        super().__init__(name, value, parents, child, id_)
        self._normid = normid
        self._year = year
        self._region = region

    @property
    def normid(self) -> str:
        return self._normid

    @property
    def year(self) -> int:
        return self._year

    @property
    def region(self) -> str:
        return self._region


class PriceIndex(MappedVariable):
    pass


class ConversionFactor(MappedVariable):
    pass


class EmissionFactor(MappedVariable):
    pass


T = TypeVar("T", bound=MappedVariable)


class FakeRepository(Generic[T]):
    # What we really have are views, not repositories. Since we only query data.
    def __init__(self, entities: Iterable[T] | None = None) -> None:
        self._entities = set[T](entities) if entities else set[T]()
        self.seen = set[T]()

    def get(self, id: str) -> T | None:
        entity = next((e for e in self._entities if e.id == id), None)
        if entity:
            self.seen.add(entity)
        return entity

    def get_by_normid(self, normid: str, year: int, region: str) -> T | None:
        entity = next(
            (
                e
                for e in self._entities
                if e.normid == normid and e.year == year and e.region == region
            ),
            None,
        )
        if entity:
            self.seen.add(entity)
        return entity


def generate_price_indices() -> Iterable[PriceIndex]:
    source = DataSource(
        "Eurostat",
        "Producer price indices dataset",
        2022,
    )
    yield PriceIndex(
        "02030000000000",
        2021,
        "SE",
        "Electric power generation, transmission and distribution",
        150,
        parents=[source],
    )
    yield PriceIndex(
        "02030000000000",
        2023,
        "SE",
        "Electric power generation, transmission and distribution",
        175,
        parents=[source],
    )


def generate_conversion_factors() -> Iterable[ConversionFactor]:
    source = DataSource(
        "IEA Energy Prices",
        "",
        2022,
    )
    yield ConversionFactor(
        "02030000000000",
        2021,
        "SE",
        "Industrial electricity",
        0.068,
        parents=[source],
    )


def generate_emission_factors() -> Iterable[EmissionFactor]:
    source = DataSource(
        "AIB",
        "",
        2022,
    )
    yield EmissionFactor(
        "02030000000000",
        2022,
        "SE",
        "Electricity",
        0.07663,
        parents=[source],
    )
