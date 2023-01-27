from __future__ import annotations
from typing import TYPE_CHECKING, Any
import uuid

from calculation_tree.model import Node

if TYPE_CHECKING:
    from calculation_tree.model import Variable


class DataSource(Node):
    def __init__(
        self,
        name: str,
        description: str | None = None,
        year: int | None = None,
        child: Variable | None = None,
        id_: uuid.UUID | None = None,
    ) -> None:
        super().__init__(name, None, child, id_)
        self._description = description
        self._year = year

    def __str__(self) -> str:
        return f"{self.name} ({self.year})"

    @property
    def description(self) -> str | None:
        return self._description

    @property
    def year(self) -> int | None:
        return self._year

    def to_dict(self) -> dict[str, Any]:
        return super()._to_dict(description=self.description, year=self.year)
