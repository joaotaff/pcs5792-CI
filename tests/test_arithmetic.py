"""Tests for basic arithmetic helpers in ``src``."""

import os
import sys
import unittest

SRC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from arithmetic_series import sum_of_arithmetic_series
from cross_multiply import cross_multiply
from product import product
from rpd import relatice_percent_difference
from series_sum import (
    sum_of_n_even_numbers,
    sum_of_n_natural_numbers,
    sum_of_n_odd_numbers,
    sum_of_square_of_n_numbers,
    var_sum,
)
from simple_interest import simple_interest


class TestArithmeticSeries(unittest.TestCase):
    def test_documented_example(self):
        # 1 + 4 + 7 + 10 = 22
        self.assertEqual(sum_of_arithmetic_series(1, 3, 4), 22)

    def test_zero_terms(self):
        self.assertEqual(sum_of_arithmetic_series(5, 2, 0), 0)

    def test_negative_term_count_is_empty_series(self):
        self.assertEqual(sum_of_arithmetic_series(5, 2, -3), 0)

    def test_constant_series(self):
        self.assertEqual(sum_of_arithmetic_series(7, 0, 5), 35)

    def test_accepts_floats(self):
        self.assertAlmostEqual(sum_of_arithmetic_series(0.5, 0.5, 3), 3.0)


class TestSimpleInterest(unittest.TestCase):
    def test_basic_interest(self):
        self.assertEqual(simple_interest(1000, 5, 2), 100.0)

    def test_zero_principal(self):
        self.assertEqual(simple_interest(0, 5, 2), 0.0)

    def test_zero_rate(self):
        self.assertEqual(simple_interest(1000, 0, 2), 0.0)

    def test_zero_time(self):
        self.assertEqual(simple_interest(1000, 5, 0), 0.0)

    def test_fractional_years(self):
        self.assertAlmostEqual(simple_interest(200, 2.5, 0.5), 2.5)


class TestCrossMultiply(unittest.TestCase):
    def test_solves_for_fourth_term(self):
        # 2/3 = 4/d  ->  d = 3 * 4 / 2 = 6
        self.assertEqual(cross_multiply(2, 4, 3), 6.0)

    def test_another_fraction(self):
        # 5/2 = 10/d -> d = 2 * 10 / 5 = 4
        self.assertEqual(cross_multiply(5, 10, 2), 4.0)

    def test_negative_values(self):
        self.assertEqual(cross_multiply(-2, 4, 3), -6.0)


class TestRelativePercentDifference(unittest.TestCase):
    def test_symmetric_difference(self):
        self.assertAlmostEqual(relatice_percent_difference(10, 20), 200 / 3)

    def test_equal_values_give_zero(self):
        self.assertEqual(relatice_percent_difference(5, 5), 0.0)

    def test_order_does_not_matter(self):
        self.assertAlmostEqual(
            relatice_percent_difference(10, 20),
            relatice_percent_difference(20, 10),
        )

    def test_opposite_values_divide_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            relatice_percent_difference(-10, 10)


class TestProduct(unittest.TestCase):
    def test_empty_iterable_is_one(self):
        self.assertEqual(product([]), 1)

    def test_list_of_integers(self):
        self.assertEqual(product([2, 3, 4]), 24)

    def test_single_element(self):
        self.assertEqual(product([9]), 9)

    def test_zero_propagates(self):
        self.assertEqual(product([1, 0, 5]), 0)

    def test_floats(self):
        self.assertAlmostEqual(product([0.5, 4]), 2.0)


class TestSeriesSum(unittest.TestCase):
    def test_var_sum_without_arguments(self):
        self.assertEqual(var_sum(), 0)

    def test_var_sum_adds_all_arguments(self):
        self.assertEqual(var_sum(1, 2, 3, 4), 10)

    def test_var_sum_rejects_non_numbers(self):
        self.assertIsNone(var_sum(1, "two", 3))

    def test_sum_of_natural_numbers(self):
        self.assertEqual(sum_of_n_natural_numbers(5), 15)
        self.assertEqual(sum_of_n_natural_numbers(1), 1)

    def test_sum_of_natural_numbers_invalid_input(self):
        self.assertIsNone(sum_of_n_natural_numbers(0))
        self.assertIsNone(sum_of_n_natural_numbers(-1))
        self.assertIsNone(sum_of_n_natural_numbers("5"))

    def test_sum_of_even_numbers(self):
        # 2 + 4 + 6 + 8 + 10 = 30
        self.assertEqual(sum_of_n_even_numbers(5), 30)
        self.assertEqual(sum_of_n_even_numbers(0), 0)

    def test_sum_of_even_numbers_invalid_input(self):
        self.assertIsNone(sum_of_n_even_numbers(-1))
        self.assertIsNone(sum_of_n_even_numbers("5"))

    def test_sum_of_odd_numbers(self):
        # 1 + 3 + 5 + 7 + 9 = 25
        self.assertEqual(sum_of_n_odd_numbers(5), 25)
        self.assertEqual(sum_of_n_odd_numbers(0), 0)

    def test_sum_of_odd_numbers_invalid_input(self):
        self.assertIsNone(sum_of_n_odd_numbers(-1))
        self.assertIsNone(sum_of_n_odd_numbers(None))

    def test_sum_of_squares(self):
        # 1 + 4 + 9 + 16 + 25 = 55
        self.assertEqual(sum_of_square_of_n_numbers(5), 55)
        self.assertEqual(sum_of_square_of_n_numbers(0), 0)

    def test_sum_of_squares_invalid_input(self):
        self.assertIsNone(sum_of_square_of_n_numbers(-1))
        self.assertIsNone(sum_of_square_of_n_numbers("5"))


if __name__ == "__main__":
    unittest.main()
