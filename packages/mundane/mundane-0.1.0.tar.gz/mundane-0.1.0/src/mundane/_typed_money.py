from ._currency import Currency
from ._money import Money
from ._typed_money_mixin import TypedMoneyMixin


class TypedMoney(TypedMoneyMixin, Money, metaclass = Currency):
	pass
