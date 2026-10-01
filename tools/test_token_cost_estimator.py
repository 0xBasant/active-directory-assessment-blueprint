import unittest
from decimal import Decimal

from token_cost_estimator import calculate, non_negative_int


class TokenCostEstimatorTests(unittest.TestCase):
    def test_sol_medium_example(self):
        result = calculate("gpt-6.1-sol", 2_000_000, 0, 800_000)
        self.assertEqual(result["input"], Decimal("4.00"))
        self.assertEqual(result["output"], Decimal("8.00"))
        self.assertEqual(result["total"], Decimal("12.00"))

    def test_cached_input(self):
        result = calculate("gpt-6-luna", 0, 1_000_000, 0)
        self.assertEqual(result["total"], Decimal("0.01"))

    def test_negative_tokens_rejected(self):
        with self.assertRaises(Exception):
            non_negative_int("-1")


if __name__ == "__main__":
    unittest.main()
