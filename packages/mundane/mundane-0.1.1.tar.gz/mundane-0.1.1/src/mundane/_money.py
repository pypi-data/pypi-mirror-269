import math
from decimal import Decimal as decimal
from types import NotImplementedType
from typing import Self, dataclass_transform, overload

from ._currency import Currency


class OverloadPaddingType1:
	pass


class OverloadPaddingType2:
	pass


@dataclass_transform(frozen_default=True)
def freeze_money[T](cls: T) -> T:
	def setattr(*args: object):
		raise AttributeError("'Money' is frozen")
	cls.__setattr__ = setattr
	return cls

@freeze_money
class Money:
	__slots__ = ('value',)
	value: decimal

	@property
	def currency(self) -> Currency:
		return type(self)  # type: ignore

	def __init__(self, value: decimal | str | int):
		if type(self) == Money:
			raise TypeError("'Money' cannot be instantiated")
		object.__setattr__(self, 'value', decimal(value))

	def __str__(self):
		return f"{self.currency} {self.value:f}"

	def __repr__(self):
		return f"{self.currency}('{self.value:f}')"

	def __hash__(self):
		return hash((self.currency, self.value))

	def __eq__(self, other: object) -> bool:
		if isinstance(other, Money):
			return (self.currency, self.value) == (other.currency, other.value)
		return NotImplemented

	@overload
	def __lt__(self, other: OverloadPaddingType1) -> NotImplementedType:
		pass

	@overload
	def __lt__(self, other: OverloadPaddingType2) -> NotImplementedType:
		pass

	def __lt__(self, other: object) -> bool | NotImplementedType:
		if not isinstance(other, Money):
			return NotImplemented
		if self.currency != other.currency:
			raise TypeError(f"'<' not supported between money in '{self.currency}' and '{other.currency}'")
		return self.value < other.value

	@overload
	def __le__(self, other: OverloadPaddingType1) -> NotImplementedType:
		pass

	@overload
	def __le__(self, other: OverloadPaddingType2) -> NotImplementedType:
		pass

	def __le__(self, other: object) -> bool | NotImplementedType:
		if not isinstance(other, Money):
			return NotImplemented
		if self.currency != other.currency:
			raise TypeError(f"'<=' not supported between money in '{self.currency}' and '{other.currency}'")
		return self.value <= other.value

	@overload
	def __gt__(self, other: OverloadPaddingType1) -> NotImplementedType:
		pass

	@overload
	def __gt__(self, other: OverloadPaddingType2) -> NotImplementedType:
		pass

	def __gt__(self, other: object) -> bool | NotImplementedType:
		if not isinstance(other, Money):
			return NotImplemented
		if self.currency != other.currency:
			raise TypeError(f"'>' not supported between money in '{self.currency}' and '{other.currency}'")
		return self.value > other.value

	@overload
	def __ge__(self, other: OverloadPaddingType1) -> NotImplementedType:
		pass

	@overload
	def __ge__(self, other: OverloadPaddingType2) -> NotImplementedType:
		pass

	def __ge__(self, other: object) -> bool | NotImplementedType:
		if not isinstance(other, Money):
			return NotImplemented
		if self.currency != other.currency:
			raise TypeError(f"'>=' not supported between money in '{self.currency}' and '{other.currency}'")
		return self.value >= other.value

	def __pos__(self) -> Self:
		return type(self)(value = +self.value)

	def __neg__(self) -> Self:
		return type(self)(value = -self.value)

	def __abs__(self) -> Self:
		return type(self)(value = abs(self.value))

	@overload
	def __add__(self, other: OverloadPaddingType1) -> NotImplementedType:
		...

	@overload
	def __add__(self, other: OverloadPaddingType2) -> NotImplementedType:
		...

	def __add__(self, other: object) -> Self | NotImplementedType:
		if not isinstance(other, Money):
			return NotImplemented
		if self.currency != other.currency:
			raise TypeError(f"'+' not supported between money in '{self.currency}' and '{other.currency}'")
		return type(self)(value = self.value + other.value)

	@overload
	def __sub__(self, other: OverloadPaddingType1) -> NotImplementedType:
		...

	@overload
	def __sub__(self, other: OverloadPaddingType2) -> NotImplementedType:
		...

	def __sub__(self, other: object) -> Self | NotImplementedType:
		if not isinstance(other, Money):
			return NotImplemented
		if self.currency != other.currency:
			raise TypeError(f"'-' not supported between money in '{self.currency}' and '{other.currency}'")
		return type(self)(value = self.value - other.value)

	@overload
	def __mul__(self, other: OverloadPaddingType1) -> NotImplementedType:
		...

	@overload
	def __mul__(self, other: int | decimal) -> Self:
		...

	def __mul__(self, other: object) -> Self | NotImplementedType:
		if isinstance(other, int) or isinstance(other, decimal):  # type: ignore
			return type(self)(value = self.value * other)
		return NotImplemented

	@overload
	def __rmul__(self, other: OverloadPaddingType1) -> NotImplementedType:
		...

	@overload
	def __rmul__(self, other: int | decimal) -> Self:
		...

	def __rmul__(self, other: object) -> Self | NotImplementedType:
		if isinstance(other, int) or isinstance(other, decimal):  # type: ignore
			return type(self)(value = self.value * other)
		return NotImplemented

	@overload
	def __truediv__(self, other: OverloadPaddingType1) -> NotImplementedType:
		...

	@overload
	def __truediv__(self, other: int | decimal) -> Self:
		...

	def __truediv__(self, other: object) -> decimal | Self | NotImplementedType:
		if isinstance(other, int) or isinstance(other, decimal):
			return type(self)(value = self.value / other)
		if not isinstance(other, Money):  # type: ignore
			return NotImplemented
		if self.currency != other.currency:
			raise TypeError(f"'/' not supported between money in '{self.currency}' and '{other.currency}'")
		return self.value / other.value

	def __round__(self, ndigits: int | None = None) -> Self:
		return type(self)(value = round(self.value, ndigits))

	def __trunc__(self) -> Self:
		return type(self)(value = math.trunc(self.value))

	def __floor__(self) -> Self:
		return type(self)(value = math.floor(self.value))

	def __ceil__(self) -> Self:
		return type(self)(value = math.ceil(self.value))
