"""R2: top-level traded_value must equal the sum of |qty x price| over all trades (abs tol 0.01).
Same contract as check_fees.check: returns {'rule_id','verdict','offending_trades'}; raises ValueError on bad shape."""
from decimal import Decimal

from check_fees import number

TOLERANCE = Decimal('0.01')


def check(ledger):
    if not isinstance(ledger, dict) or not isinstance(ledger.get('trades'), list) or not ledger['trades']:
        raise ValueError('Ledger must contain a nonempty trades array')
    if 'traded_value' not in ledger:
        raise ValueError('Ledger must include traded_value')
    total = Decimal(0)
    for trade in ledger['trades']:
        if not isinstance(trade, dict):
            raise ValueError('Every trade must be an object')
        qty, price = number(trade.get('qty')), number(trade.get('price'))
        if qty <= 0 or price <= 0:
            raise ValueError('Quantity and price must be positive')
        total += qty * price
    found = number(ledger['traded_value'])
    bad = abs(found - total) > TOLERANCE
    offending = [{'field': 'traded_value', 'expected': str(total), 'found': str(found)}] if bad else []
    return {'rule_id': 'R2', 'verdict': 'fail' if bad else 'pass', 'offending_trades': offending}
