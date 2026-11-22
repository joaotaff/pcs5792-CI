"""Tests for sequence helpers in ``src``."""

import collections
import contextlib
import io
import os
import sys
import unittest

SRC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from fibonacci import (
    fibonacci_dynamic,
    fibonacci_iterative,
    fibonacci_recursive,
    fibonacci_recursive_cached,
)
from pascal_triangle import make_pascal_triangle
from unique_elements import frequency, unique_elements


class TestFibonacci(unittest.TestCase):
    def test_recursive(self):
        expected = {1: 0, 2: 1, 3: 1, 4: 2, 5: 3, 10: 34}
        for n, value in expected.items():
            with self.subTest(n=n):
                self.assertEqual(fibonacci_recursive(n), value)

    def test_recursive_negative_input_returns_none(self):
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            result = fibonacci_recursive(-1)
        self.assertIsNone(result)
        self.assertIn("Invalid input", buffer.getvalue())

    def test_recursive_cached(self):
        expected = {0: 0, 1: 1, 2: 1, 3: 2, 10: 55, 50: 12586269025}
        for n, value in expected.items():
            with self.subTest(n=n):
                self.assertEqual(fibonacci_recursive_cached(n), value)

    def test_iterative(self):
        expected = {1: 1, 2: 1, 3: 2, 10: 55, 50: 12586269025}
        for n, value in expected.items():
            with self.subTest(n=n):
                self.assertEqual(fibonacci_iterative(n), value)

    def test_dynamic(self):
        expected = {1: 1, 2: 1, 3: 2, 10: 55, 39: 63245986}
        for n, value in expected.items():
            with self.subTest(n=n):
                self.assertEqual(fibonacci_dynamic(n), value)


class TestPascalTriangle(unittest.TestCase):
    def test_five_rows(self):
        expected = [
            [1],
            [1, 1],
            [1, 2, 1],
            [1, 3, 3, 1],
            [1, 4, 6, 4, 1],
        ]
        self.assertEqual(make_pascal_triangle(5), expected)

    def test_two_rows(self):
        self.assertEqual(make_pascal_triangle(2), [[1], [1, 1]])

    def test_sixth_row(self):
        triangle = make_pascal_triangle(6)
        self.assertEqual(triangle[-1], [1, 5, 10, 10, 5, 1])
        self.assertEqual(len(triangle), 6)


class TestUniqueElements(unittest.TestCase):
    def test_removes_duplicates_preserving_order(self):
        self.assertEqual(unique_elements([3, 1, 3, 2, 1]), [3, 1, 2])

    def test_empty_list(self):
        self.assertEqual(unique_elements([]), [])

    def test_strings(self):
        self.assertEqual(
            unique_elements(["a", "b", "a", "c", "b"]),
            ["a", "b", "c"],
        )

    def test_frequency(self):
        self.assertEqual(
            frequency([1, 1, 2, 3, 3, 3]),
            collections.Counter({1: 2, 2: 1, 3: 3}),
        )

    def test_frequency_of_strings(self):
        self.assertEqual(
            frequency("hello"),
            collections.Counter({"h": 1, "e": 1, "l": 2, "o": 1}),
        )


if __name__ == "__main__":
    unittest.main()
