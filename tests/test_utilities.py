"""Tests for small utility helpers in ``src``."""

import math
import os
import random
import sys
import unittest
from unittest import mock

SRC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

import estimate_pi
from even_odd import is_even, is_odd
from zeros import zeros


class TestEvenOdd(unittest.TestCase):
    def test_even_numbers(self):
        for number in (0, 2, -4, 100):
            with self.subTest(number=number):
                self.assertTrue(is_even(number))
                self.assertFalse(is_odd(number))

    def test_odd_numbers(self):
        for number in (1, 3, -3, 99):
            with self.subTest(number=number):
                self.assertFalse(is_even(number))
                self.assertTrue(is_odd(number))

    def test_even_and_odd_are_complements(self):
        for number in range(-10, 11):
            with self.subTest(number=number):
                self.assertNotEqual(is_even(number), is_odd(number))


class TestZeros(unittest.TestCase):
    def test_flat_array(self):
        self.assertEqual(zeros(3), [0, 0, 0])

    def test_flat_array_of_zero_length(self):
        self.assertEqual(zeros(0), [])

    def test_two_dimensional_array(self):
        self.assertEqual(zeros((2, 3)), [[0, 0, 0], [0, 0, 0]])

    def test_single_row_returns_flat_array(self):
        self.assertEqual(zeros((1, 3)), [0, 0, 0])

    def test_zero_rows(self):
        self.assertEqual(zeros((0, 3)), [])

    def test_empty_rows(self):
        self.assertEqual(zeros((2, 0)), [[], []])


class TestEstimatePi(unittest.TestCase):
    def test_all_points_inside_circle(self):
        # Every sampled point equals the centre (1, 1), so all are inside.
        with mock.patch.object(estimate_pi.random, "uniform", return_value=1.0):
            self.assertEqual(estimate_pi.estimate(100), 4.0)

    def test_no_points_inside_circle(self):
        # (0, 0) is sqrt(2) away from the centre, outside the unit circle.
        with mock.patch.object(estimate_pi.random, "uniform", return_value=0.0):
            self.assertEqual(estimate_pi.estimate(100), 0.0)

    def test_statistical_estimate_is_close_to_pi(self):
        random.seed(12345)
        self.assertAlmostEqual(estimate_pi.estimate(20000), math.pi, delta=0.15)

    def test_estimate_uses_requested_number_of_points(self):
        with mock.patch.object(
            estimate_pi.random, "uniform", return_value=1.0
        ) as uniform:
            estimate_pi.estimate(7)
        self.assertEqual(uniform.call_count, 14)  # two coordinates per point


if __name__ == "__main__":
    unittest.main()
