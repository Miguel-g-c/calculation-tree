from __future__ import annotations
from decimal import Decimal
from typing import Any
import uuid

from calculation_tree.model import Node, Operation


NUMERIC = float | int | Decimal


class Variable(Node):
    def __init__(
        self,
        name: str,
        value: NUMERIC,
        parents: list[Node] | None = None,
        child: Node | None = None,
        id_: uuid.UUID | None = None,
    ) -> None:
        super().__init__(name, parents, child, id_)
        self._value = float(value)

    def __int__(self) -> int:
        return int(self.value)

    def __float__(self) -> float:
        return self.value

    def __repr__(self) -> str:
        return f"Variable({self.name}, {self.value:.2f})"

    def __str__(self) -> str:
        return f"{self.name} = {self.value}"

    def __add__(self, other: Variable) -> Variable:
        operation = Operation("add", parents=[self, other])
        self._child = operation
        other._child = operation
        new_variable = Variable(
            f"{self.name} + {other.name}",
            self.value + other.value,
            parents=[operation],
        )
        operation._child = new_variable
        return new_variable

    def __sub__(self, other: Variable) -> Variable:
        operation = Operation("sub", parents=[self, other])
        self._child = operation
        other._child = operation
        new_variable = Variable(
            f"{self.name} - {other.name}",
            self.value - other.value,
            parents=[operation],
        )
        operation._child = new_variable
        return new_variable

    def __mul__(self, other: Variable) -> Variable:
        operation = Operation("mul", parents=[self, other])
        self._child = operation
        other._child = operation
        new_variable = Variable(
            f"{self.name} * {other.name}",
            self.value * other.value,
            parents=[operation],
        )
        operation._child = new_variable
        return new_variable

    def __truediv__(self, other: Variable) -> Variable:
        operation = Operation("truediv", parents=[self, other])
        self._child = operation
        other._child = operation
        new_variable = Variable(
            f"{self.name} / {other.name}",
            self.value / other.value,
            parents=[operation],
        )
        operation._child = new_variable
        return new_variable

    def __pow__(self, other: Variable) -> Variable:
        operation = Operation("pow", parents=[self, other])
        self._child = operation
        other._child = operation
        new_variable = Variable(
            f"{self.name} ** {other.name}",
            self.value**other.value,
            parents=[operation],
        )
        operation._child = new_variable
        return new_variable

    def __neg__(self) -> Variable:
        operation = Operation("neg", parents=[self])
        self._child = operation
        new_variable = Variable(
            f"-{self.name}",
            -self.value,
            parents=[operation],
        )
        operation._child = new_variable
        return new_variable

    def __abs__(self) -> Variable:
        operation = Operation("abs", parents=[self])
        self._child = operation
        new_variable = Variable(
            f"abs({self.name})",
            abs(self.value),
            parents=[operation],
        )
        operation._child = new_variable
        return new_variable

    @property
    def value(self) -> float:
        return self._value

    def to_dict(self) -> dict[str, Any]:
        return super()._to_dict(value=self.value)
