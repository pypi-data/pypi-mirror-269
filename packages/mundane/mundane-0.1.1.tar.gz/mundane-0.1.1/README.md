# mundane
Pythonic Money class. Correct. Type-safe. Matches expectations.

## Installation
```sh
pip install mundane
```

Required Python version: 3.12.

## Usage
```py
>>> from mundane import EUR, PLN, Money
>>> PLN(50) < PLN(100)
True
>>> PLN(50) < EUR(50)
TypeError: '<' not supported between money in 'PLN' and 'EUR'
>>> PLN(50) / 2
PLN('25')
>>> def do_something_with_money(money: Money):
...     print(money)
...
>>> do_something_with_money(PLN(25))
PLN 25
>>> do_something_with_money(EUR(50))
EUR 50
```

See [tests/test_money.py](tests/test_money.py) for more examples.

Supported operations (a and b are money instances with matching currency):
* a == b, a != b, a < b, a <= b, a > b, a >= b
* +a, -a, abs(a)
* a + b, a - b, 2 * a, a * 2, a / 2, a / b
* round(a), round(a, 2), math.trunc(a), math.floor(a), math.ceil(a)
* str(a), repr(a), hash(a)

## Define your own currency
```py
from mundane import TypedMoney

class BTC(TypedMoney):
    pass

print(BTC('0.0000000000000000000000000001'))
# BTC 0.0000000000000000000000000001
```
