from decimal import Decimal as decimal

from ._money import Money
from ._typed_money_mixin import TypedMoneyMixin


class AnyMoney(TypedMoneyMixin, Money):
	__slots__ = ()

	def __init__(self, value: decimal | str | int):
		raise TypeError("AnyMoney cannot be instantiated")
