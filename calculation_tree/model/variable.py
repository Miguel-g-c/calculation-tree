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
        new_variable = self.__operate_with(
            other, "add", f"{self.name} + {other.name}", self.value + other.value
        )
        return new_variable

    def __sub__(self, other: Variable) -> Variable:
        new_variable = self.__operate_with(
            other, "sub", f"{self.name} - {other.name}", self.value - other.value
        )
        return new_variable

    def __mul__(self, other: Variable) -> Variable:
        new_variable = self.__operate_with(
            other, "mul", f"{self.name} * {other.name}", self.value * other.value
        )
        return new_variable

    def __truediv__(self, other: Variable) -> Variable:
        new_variable = self.__operate_with(
            other, "truediv", f"{self.name} / {other.name}", self.value / other.value
        )
        return new_variable

    def __pow__(self, other: Variable) -> Variable:
        new_variable = self.__operate_with(
            other, "pow", f"{self.name} ** {other.name}", self.value**other.value
        )
        return new_variable

    def __neg__(self) -> Variable:
        new_variable = self.__operate("neg", f"-{self.name}", -self.value)
        return new_variable

    def __abs__(self) -> Variable:
        new_variable = self.__operate("abs", f"abs({self.name})", abs(self.value))
        return new_variable

    @property
    def value(self) -> float:
        return self._value

    def to_dict(self) -> dict[str, Any]:
        return super()._to_dict(value=self.value)

    def __operate(self, op_name: str, var_name: str, var_value: NUMERIC) -> Variable:
        operation = Operation(op_name, parents=[self])
        self._child = operation
        new_variable = Variable(
            var_name,
            var_value,
            parents=[operation],
        )
        operation._child = new_variable
        return new_variable

    def __operate_with(
        self, other: Variable, op_name: str, var_name: str, var_value: NUMERIC
    ) -> Variable:
        if not isinstance(other, Variable):
            raise TypeError(
                f"Unsupported operand type(s) for: 'Variable' and '{type(other)}'"
            )
        operation = Operation(op_name, parents=[self, other])
        self._child = operation
        other._child = operation
        new_variable = Variable(var_name, var_value, parents=[operation])
        operation._child = new_variable
        return new_variable
