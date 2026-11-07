"""Check synthetic per-trade fees. Exit 0 pass, 1 fail, 2 invalid input."""
import argparse
import csv
import json
from decimal import Decimal, InvalidOperation
from pathlib import Path

RATE = Decimal('0.0005')
TOLERANCE = Decimal('0.01')


def number(value):
    if isinstance(value, bool) or value is None:
        raise ValueError('Expected a finite number')
    try:
        result = Decimal(str(value))
    except InvalidOperation as error:
        raise ValueError('Expected a finite number') from error
    if not result.is_finite():
        raise ValueError('Expected a finite number')
    return result


def check(ledger):
    if not isinstance(ledger, dict) or not isinstance(ledger.get('trades'), list) or not ledger['trades']:
        raise ValueError('Ledger must contain a nonempty trades array')
    offending = []
    ids = set()
    for trade in ledger['trades']:
        if not isinstance(trade, dict):
            raise ValueError('Every trade must be an object')
        trade_id = trade.get('id')
        if isinstance(trade_id, bool) or not isinstance(trade_id, (str, int)) or trade_id in ids:
            raise ValueError('Trade IDs must be unique strings or integers')
        ids.add(trade_id)
        if not isinstance(trade.get('symbol'), str) or not trade['symbol'].strip() or trade.get('side') not in ('buy', 'sell'):
            raise ValueError('Every trade needs a symbol and buy/sell side')
        qty, price = number(trade.get('qty')), number(trade.get('price'))
        if qty <= 0 or price <= 0:
            raise ValueError('Quantity and price must be positive')
        expected = qty * price * RATE
        found = trade.get('fee')
        if found is None:
            offending.append({'id': trade_id, 'expected_fee': str(expected), 'found_fee': None})
            continue
        fee = number(found)
        if fee < 0 or abs(fee - expected) > TOLERANCE:
            offending.append({'id': trade_id, 'expected_fee': str(expected), 'found_fee': str(fee)})
    # shortcut: validates per-trade costs only; add a returns contract before claiming net-return validation.
    return {'rule_id': 'R1', 'verdict': 'fail' if offending else 'pass', 'offending_trades': offending}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('ledger', type=Path)
    args = parser.parse_args()
    try:
        with args.ledger.open() as source:
            ledger = {'trades': list(csv.DictReader(source))} if args.ledger.suffix.lower() == '.csv' else json.load(source)
        result = check(ledger)
    except (OSError, ValueError, TypeError, ArithmeticError) as error:
        print(json.dumps({'verdict': 'escalate', 'error': str(error)}))
        return 2
    print(json.dumps(result))
    return 1 if result['verdict'] == 'fail' else 0


if __name__ == '__main__':
    raise SystemExit(main())
