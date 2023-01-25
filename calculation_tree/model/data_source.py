from __future__ import annotations
from typing import TYPE_CHECKING
import uuid

from calculation_tree.model import Node

if TYPE_CHECKING:
    from calculation_tree.model import Variable


class DataSource(Node):
    def __init__(
        self,
        name: str,
        child: Variable | None = None,
        id_: uuid.UUID | None = None,
    ) -> None:
        super().__init__(name, None, child, id_)

    def __str__(self) -> str:
        return f"{self.name}"
