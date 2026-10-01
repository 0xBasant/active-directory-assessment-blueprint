#!/usr/bin/env python3
"""Estimate model token charges for planning purposes.

Pricing is a dated repository snapshot, not a billing API. Counts are aggregate
usage across Standard requests with at most 272K input tokens each. Output tokens
include billed reasoning. Long-context, processing-tier, regional, cache-write,
tool, storage, network, platform, and human cost adjustments are excluded.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from decimal import Decimal


PRICING_DATE = "2026-10-01"


@dataclass(frozen=True)
class Price:
    input_per_million: Decimal
    cached_input_per_million: Decimal
    output_per_million: Decimal


PRICES = {
    "gpt-6-luna": Price(Decimal("0.10"), Decimal("0.01"), Decimal("0.50")),
    "gpt-6.1-sol": Price(Decimal("2.00"), Decimal("0.10"), Decimal("10.00")),
    "gpt-6-astra": Price(Decimal("10.00"), Decimal("1.00"), Decimal("50.00")),
}


def non_negative_int(value: str) -> int:
    parsed = int(value)
    if parsed < 0:
        raise argparse.ArgumentTypeError("token counts must be non-negative")
    return parsed


def calculate(model: str, input_tokens: int, cached_tokens: int, output_tokens: int) -> dict[str, Decimal]:
    price = PRICES[model]
    million = Decimal(1_000_000)
    components = {
        "input": Decimal(input_tokens) / million * price.input_per_million,
        "cached_input": Decimal(cached_tokens) / million * price.cached_input_per_million,
        "output": Decimal(output_tokens) / million * price.output_per_million,
    }
    components["total"] = sum(components.values(), Decimal("0"))
    return components


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(f"Estimate aggregate Standard short-context token charges using the {PRICING_DATE} "
                     "snapshot. Each underlying request must have at most 272K input tokens.")
    )
    parser.add_argument("--model", choices=sorted(PRICES), required=True)
    parser.add_argument("--input-tokens", type=non_negative_int, default=0, help="Uncached input tokens")
    parser.add_argument("--cached-input-tokens", type=non_negative_int, default=0)
    parser.add_argument(
        "--output-tokens",
        type=non_negative_int,
        default=0,
        help="Visible output plus billed reasoning tokens",
    )
    args = parser.parse_args()

    costs = calculate(args.model, args.input_tokens, args.cached_input_tokens, args.output_tokens)
    print(f"Pricing snapshot: {PRICING_DATE}")
    print(f"Model: {args.model}")
    print(f"Uncached input: ${costs['input']:.6f}")
    print(f"Cached input:   ${costs['cached_input']:.6f}")
    print(f"Output:         ${costs['output']:.6f}")
    print(f"Estimated total:${costs['total']:.6f}")
    print("Assumes aggregate Standard usage; each request has at most 272K input tokens.")
    print("Excludes tier/region adjustments, cache writes, tools, storage, networking, platform, and labor.")


if __name__ == "__main__":
    main()
