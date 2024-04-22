import math
import random
import unittest
from decimal import Decimal as decimal
from typing import assert_type, cast

from mundane import Money, AnyMoney, TypedMoney, PLN, EUR
from mundane import USD as OfficialUSD


class TestMoney(unittest.TestCase):

	def test_basic(self):
		try:
			Money(50)
		except TypeError:
			pass
		else:
			assert False
		assert_type(PLN(50), PLN)
		assert isinstance(PLN(50), PLN)
		assert isinstance(PLN(50), Money)
		assert PLN(50).value == 50
		assert PLN(50).currency == 'PLN'
		assert isinstance(PLN(50), PLN)
		assert isinstance(EUR(50), EUR)
		assert not isinstance(PLN(50), EUR)
		assert not isinstance(EUR(50), PLN)

	def test_frozen(self):
		try:
			EUR(50).currency = 'eee'  # type: ignore
		except AttributeError:
			pass
		else:
			assert False

		try:
			EUR(50).value = decimal(3)  # type: ignore
		except AttributeError:
			pass
		else:
			assert False

		try:
			EUR(50).some_other = 15  # type: ignore
		except AttributeError:
			pass
		else:
			assert False

	def test_slots(self):
		try:
			EUR(50).__dict__
		except AttributeError:
			pass
		else:
			assert False

	def test_str(self):
		assert str(PLN(50).currency) == 'PLN'
		assert repr(PLN(50).currency) == '\'PLN\''
		assert str(PLN(50)) == 'PLN 50'
		assert repr(PLN(50)) == 'PLN(\'50\')'
		assert hash(PLN(50))
		assert str(EUR('0.0000000000000000000001')) == 'EUR 0.0000000000000000000001'
		assert repr(EUR('0.0000000000000000000001')) == 'EUR(\'0.0000000000000000000001\')'

	def test_eq(self):
		assert_type(PLN(50) == PLN(100), bool)
		assert PLN(50) == PLN('50') == PLN(decimal('50'))
		assert PLN(50) != PLN(100)
		assert PLN(50) != EUR(50)

		assert PLN(50).currency == 'PLN'

	def test_order(self):
		assert_type(PLN(50) < PLN(100), bool)
		assert PLN(50) < PLN(100)
		assert not PLN(50) < PLN(50)
		assert not PLN(50) < PLN(20)
		assert PLN(50) > PLN(20)
		assert not PLN(50) > PLN(50)
		assert not PLN(50) > PLN(100)
		assert PLN(50) <= PLN(50)
		assert PLN(50) <= PLN(100)
		assert not PLN(50) <= PLN(20)
		assert PLN(50) >= PLN(50)
		assert PLN(50) >= PLN(20)
		assert not PLN(50) >= PLN(100)
		try:
			assert PLN(50) < EUR(50)  # type: ignore
		except TypeError:
			pass
		else:
			assert False

	def test_math(self):
		assert_type(+PLN(50), PLN)
		assert +PLN(50) == PLN(50)
		assert +PLN(-50) == PLN(-50)

		assert_type(-PLN(50), PLN)
		assert -PLN(50) == PLN(-50)
		assert -PLN(-50) == PLN(50)

		assert_type(abs(PLN(50)), PLN)
		assert abs(PLN(50)) == PLN(50)
		assert abs(PLN(-50)) == PLN(50)

		assert_type(PLN(50) + PLN(100), PLN)
		assert PLN(50) + PLN(100) == PLN(150)

		try:
			PLN(50) + EUR(100)  # type: ignore
		except TypeError:
			pass
		else:
			assert False

		try:
			PLN(50) + 100  # type: ignore
		except TypeError:
			pass
		else:
			assert False

		assert_type(PLN(50) - PLN(100), PLN)
		assert PLN(50) - PLN(100) == PLN(-50)

		try:
			PLN(50) - 100  # type: ignore
		except TypeError:
			pass
		else:
			assert False

		assert_type(PLN(50) * 2, PLN)
		assert PLN(50) * 2 == PLN(100)

		assert_type(2 * PLN(50), PLN)
		assert 2 * PLN(50) == PLN(100)

		try:
			PLN(2) * PLN(50)  # type: ignore
		except TypeError:
			pass
		else:
			assert False

		try:
			EUR(2) * PLN(50)  # type: ignore
		except TypeError:
			pass
		else:
			assert False

		assert_type(PLN(50) / 2, PLN)
		assert PLN(50) / 2 == PLN(25)

		assert_type(PLN(50) / PLN(2), decimal)
		assert PLN(50) / PLN(2) == decimal(25)

		try:
			PLN(50) / EUR(2)  # type: ignore
		except TypeError:
			pass
		else:
			assert False

		assert_type(round(PLN('50.123')), PLN)
		assert round(PLN('50.123')) == PLN(50)

		assert_type(round(PLN('50.5')), PLN)
		assert round(PLN('50.5')) == PLN(50)

		assert_type(round(PLN('-50.5')), PLN)
		assert round(PLN('-50.5')) == PLN(-50)

		assert_type(round(PLN('50.123'), 2), PLN)
		assert round(PLN('50.123'), 2) == PLN('50.12')

		assert_type(math.trunc(PLN('50.123')), PLN)
		assert math.trunc(PLN('50.123')) == PLN(50)

		assert_type(math.trunc(PLN('-50.123')), PLN)
		assert math.trunc(PLN('-50.123')) == PLN(-50)

		assert_type(math.floor(PLN('50.123')), PLN)
		assert math.floor(PLN('50.123')) == PLN(50)

		assert_type(math.floor(PLN('-50.123')), PLN)
		assert math.floor(PLN('-50.123')) == PLN(-51)

		assert_type(math.ceil(PLN('50.123')), PLN)
		assert math.ceil(PLN('50.123')) == PLN(51)

		assert_type(math.ceil(PLN('50.123')), PLN)
		assert math.ceil(PLN('-50.123')) == PLN(-50)

	def test_generic_type(self):
		val = PLN(50) if random.randrange(0, 2) else EUR(100)
		assert_type(val, PLN | EUR)

		def take_money_strict(money: Money):
			# Type checker should block this, but it should work in runtime.
			assert money + money  # type: ignore
			assert money / money  # type: ignore
			assert money <= money  # type: ignore
			assert money.currency in {'PLN', 'EUR'}

		def take_money(money: AnyMoney):
			assert money + money
			assert money / money
			assert money <= money
			assert money.currency in {'PLN', 'EUR'}

		take_money_strict(val)
		take_money(val)  # type: ignore
		take_money(cast(AnyMoney, val))

	def test_currencies_with_same_name(self):

		class USD(TypedMoney):
			pass

		assert str(USD(5).currency) == str(OfficialUSD(5).currency)
		assert USD(5) != OfficialUSD(5)
		assert USD(5).currency != OfficialUSD(5).currency

		try:
			USD(5) + OfficialUSD(5)  # type: ignore
		except TypeError:
			pass
		else:
			assert False
