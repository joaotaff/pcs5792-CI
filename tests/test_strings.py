"""Tests for string helpers in ``src``."""

import os
import sys
import unittest

SRC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from levenshtein_distance import levenshtein
from roman_to_integer import roman_to_int


class TestLevenshtein(unittest.TestCase):
    def test_documented_example(self):
        self.assertEqual(levenshtein("kitten", "sitting"), 3)

    def test_identical_strings(self):
        self.assertEqual(levenshtein("abc", "abc"), 0)

    def test_empty_strings(self):
        self.assertEqual(levenshtein("", ""), 0)

    def test_one_empty_string(self):
        self.assertEqual(levenshtein("abc", ""), 3)
        self.assertEqual(levenshtein("", "abc"), 3)

    def test_is_symmetric(self):
        self.assertEqual(levenshtein("flaw", "lawn"), levenshtein("lawn", "flaw"))

    def test_single_substitution(self):
        self.assertEqual(levenshtein("cat", "cut"), 1)


class TestRomanToInteger(unittest.TestCase):
    def test_single_symbols(self):
        expected = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
        for numeral, value in expected.items():
            with self.subTest(numeral=numeral):
                self.assertEqual(roman_to_int(numeral), value)

    def test_additive_numerals(self):
        self.assertEqual(roman_to_int("III"), 3)
        self.assertEqual(roman_to_int("XXVII"), 27)
        self.assertEqual(roman_to_int("LVIII"), 58)

    def test_subtractive_numerals(self):
        self.assertEqual(roman_to_int("IV"), 4)
        self.assertEqual(roman_to_int("IX"), 9)
        self.assertEqual(roman_to_int("MCMXCIV"), 1994)

    def test_empty_string_raises(self):
        with self.assertRaises(IndexError):
            roman_to_int("")


if __name__ == "__main__":
    unittest.main()
