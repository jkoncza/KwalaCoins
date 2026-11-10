#!/usr/bin/env python3
"""Sums the KwalaCoins emission schedule exactly as GetBlockSubsidy() does."""
COIN = 10**8
INTERVAL = 2_500_000
total = 0
for halvings in range(64):
    total += ((100 * COIN) >> halvings) * INTERVAL
print(f"Total emission: {total / COIN:,.8f} KWALA")
print(f"MAX_MONEY     : {500_000_000:,} KWALA")
assert total <= 500_000_000 * COIN
