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
        id_=uuid.UUID("8d4ac02a-bb32-4c29-b0b8-201062d828bd"),
    )
    yield PriceIndex(
        "02030000000000",
        2021,
        "SE",
        "Electric power generation, transmission and distribution",
        150,
        id_=uuid.UUID("fb6f139d-ec08-4e1b-bcb2-422d5dc32d55"),
        parents=[source],
    )
    yield PriceIndex(
        "02030000000000",
        2023,
        "SE",
        "Electric power generation, transmission and distribution",
        175,
        id_=uuid.UUID("35fe5f8b-88bc-46b2-a6cb-f77bbf4f454c"),
        parents=[source],
    )


def generate_conversion_factors() -> Iterable[ConversionFactor]:
    source = DataSource(
        "IEA Energy Prices",
        "",
        2022,
        id_=uuid.UUID("717b3be3-8044-4728-ac14-4f3de8a4b76c"),
    )
    yield ConversionFactor(
        "02030000000000",
        2021,
        "SE",
        "Industrial electricity",
        0.068,
        parents=[source],
        id_=uuid.UUID("a9c8cb1a-8e02-4b53-bf1f-6a6b9600a77b"),
    )


def generate_emission_factors() -> Iterable[EmissionFactor]:
    source = DataSource(
        "AIB",
        "",
        2022,
        id_=uuid.UUID("74c5676d-5b8b-43ae-b092-3203a34dfb6e"),
    )
    yield EmissionFactor(
        "02030000000000",
        2022,
        "SE",
        "Electricity",
        0.07663,
        parents=[source],
        id_=uuid.UUID("0904eaa8-c828-4f20-bb7c-cf9d7556feb3"),
    )
