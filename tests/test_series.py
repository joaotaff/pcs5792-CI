"""Tests for series-based helpers in ``src``."""

import math
import os
import sys
import unittest

SRC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from louville_distance import louville_distance
from taylor_series import (
    ln_one_plus_x,
    taylor_arctan,
    taylor_cosine,
    taylor_exp,
    taylor_sine,
)


class TestTaylorSeries(unittest.TestCase):
    def test_ln_one_plus_x(self):
        self.assertAlmostEqual(ln_one_plus_x(0.5, 200), math.log(1.5), places=10)

    def test_ln_one_plus_zero(self):
        self.assertEqual(ln_one_plus_x(0), 0)

    def test_sine(self):
        self.assertAlmostEqual(taylor_sine(0.5), math.sin(0.5), places=12)

    def test_sine_of_zero(self):
        self.assertEqual(taylor_sine(0), 0)

    def test_cosine(self):
        self.assertAlmostEqual(taylor_cosine(0.5), math.cos(0.5), places=12)

    def test_cosine_of_zero(self):
        self.assertAlmostEqual(taylor_cosine(0), 1.0)

    def test_arctangent(self):
        self.assertAlmostEqual(taylor_arctan(0.5, 100), math.atan(0.5), places=12)

    def test_exponential(self):
        self.assertAlmostEqual(taylor_exp(1), math.e, places=12)

    def test_exponential_of_zero(self):
        self.assertAlmostEqual(taylor_exp(0), 1.0)


class TestLouvilleDistance(unittest.TestCase):
    def test_known_distances(self):
        # factorial(i) - factorial(i - 1), with the first entry forced to 1
        self.assertEqual(louville_distance(5), [1, 1, 4, 18, 96])

    def test_single_value(self):
        self.assertEqual(louville_distance(1), [1])

    def test_length_matches_precision(self):
        for precision in (1, 3, 8):
            with self.subTest(precision=precision):
                self.assertEqual(len(louville_distance(precision)), precision)

    def test_first_entries(self):
        self.assertEqual(louville_distance(3), [1, 1, 4])


if __name__ == "__main__":
    unittest.main()
