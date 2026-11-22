"""Tests for number-theory helpers in ``src``."""

import importlib.util
import os
import pathlib
import sys
import unittest
import warnings

SRC = pathlib.Path(__file__).resolve().parent.parent / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from amicable_and_incompletely_amicable import (
    amicable_numbers,
    incompletely_amicable_numbers,
    sum_proper_divisors,
)
from armstrong import armstrong_number
from binomial_coefficient import binomial_coefficient
from combination import combination, combinations
from common_divisors import gcd, gcd_recursive, lcm, lcm_trial
from factorial import factorial, factorial_approximate, factorial_recursion
from find_divisors import find_divisors
from find_factors import find_factors, prime_factors
from find_primes import find_primes_old, find_primes_sieve, prime_check
from leap_year import is_leap
from liouville_function import liouville_function
from natural_numbers import is_natural_num
from perfect_number import perfect_number
from perfect_square import per_sqr
from permutation import permutations, permutations_
from prime_factor import prime_factors as prime_factors_duplicate
from totient import totient
from count_digits import count_digits

def _load(filename, module_name):
    """Load a module whose filename is not a valid Python identifier."""
    spec = importlib.util.spec_from_file_location(module_name, SRC / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


compute_xor = _load("compute_xor_1-to-n.py", "compute_xor_1_to_n").compute_xor
n_nacci = _load("n-nacci.py", "n_nacci").n_nacci


class TestAmicableNumbers(unittest.TestCase):
    def test_sum_of_proper_divisors(self):
        self.assertEqual(sum_proper_divisors(6), 6)
        self.assertEqual(sum_proper_divisors(220), 284)
        self.assertEqual(sum_proper_divisors(284), 220)

    def test_known_amicable_pair(self):
        self.assertTrue(amicable_numbers(220, 284))
        self.assertTrue(amicable_numbers(284, 220))

    def test_non_amicable_pair(self):
        self.assertFalse(amicable_numbers(220, 221))

    def test_incompletely_amicable_pair(self):
        # proper divisors of both 6 and 25 sum to 6
        self.assertTrue(incompletely_amicable_numbers(6, 25))
        self.assertFalse(incompletely_amicable_numbers(6, 10))


class TestArmstrongNumbers(unittest.TestCase):
    def test_three_digit_armstrong_numbers(self):
        for number in (153, 370, 371, 407):
            with self.subTest(number=number):
                self.assertTrue(armstrong_number(number))

    def test_non_armstrong_numbers(self):
        for number in (100, 123, 406):
            with self.subTest(number=number):
                self.assertFalse(armstrong_number(number))

    def test_zero(self):
        self.assertTrue(armstrong_number(0))

    @unittest.expectedFailure
    def test_four_digit_armstrong_number(self):
        # 1634 = 1^4 + 6^4 + 3^4 + 4^4, but the implementation hard-codes ** 3.
        self.assertTrue(armstrong_number(1634))


class TestBinomialCoefficient(unittest.TestCase):
    def test_known_values(self):
        self.assertEqual(binomial_coefficient(5, 2), 10)
        self.assertEqual(binomial_coefficient(10, 5), 252)

    def test_boundaries(self):
        self.assertEqual(binomial_coefficient(5, 0), 1)
        self.assertEqual(binomial_coefficient(5, 5), 1)


class TestCombination(unittest.TestCase):
    def test_known_values(self):
        self.assertEqual(combination(5, 2), 10)
        self.assertEqual(combination(5, 3), 10)
        self.assertEqual(combination(10, 5), 252)

    def test_boundaries(self):
        self.assertEqual(combination(5, 0), 1)
        self.assertEqual(combination(5, 5), 1)

    def test_combinations_returns_float(self):
        self.assertEqual(combinations(5, 2), 10.0)


class TestCommonDivisors(unittest.TestCase):
    def test_gcd(self):
        self.assertEqual(gcd(48, 18), 6)
        self.assertEqual(gcd(18, 48), 6)
        self.assertEqual(gcd(7, 13), 1)

    def test_gcd_recursive(self):
        self.assertEqual(gcd_recursive(48, 18), 6)
        self.assertEqual(gcd_recursive(0, 5), 5)

    def test_lcm(self):
        self.assertEqual(lcm(4, 6), 12)
        self.assertEqual(lcm(3, 5), 15)

    def test_lcm_trial(self):
        self.assertEqual(lcm_trial(4, 6), 12)
        self.assertEqual(lcm_trial(6, 4), 12)


class TestComputeXor(unittest.TestCase):
    def test_pattern(self):
        expected = {0: 0, 1: 1, 2: 3, 3: 0, 4: 4, 5: 1, 6: 7, 7: 0, 8: 8}
        for n, value in expected.items():
            with self.subTest(n=n):
                self.assertEqual(compute_xor(n), value)

    def test_matches_naive_fold(self):
        for n in range(0, 40):
            with self.subTest(n=n):
                naive = 0
                for i in range(1, n + 1):
                    naive ^= i
                self.assertEqual(compute_xor(n), naive)


class TestCountDigits(unittest.TestCase):
    def test_zero_has_one_digit(self):
        self.assertEqual(count_digits(0), 1)

    def test_single_digit(self):
        self.assertEqual(count_digits(7), 1)

    def test_multiple_digits(self):
        self.assertEqual(count_digits(12345), 5)
        self.assertEqual(count_digits(100), 3)


class TestFactorial(unittest.TestCase):
    def test_iterative_factorial(self):
        self.assertEqual(factorial(0), 1)
        self.assertEqual(factorial(1), 1)
        self.assertEqual(factorial(5), 120)
        self.assertEqual(factorial(10), 3628800)

    def test_approximate_factorial(self):
        self.assertAlmostEqual(factorial_approximate(0), 1)
        self.assertAlmostEqual(factorial_approximate(5), 120, places=6)

    def test_recursive_factorial_zero(self):
        self.assertEqual(factorial_recursion(0), 1)

    def test_recursive_factorial_positive(self):
        self.assertEqual(factorial_recursion(5), 120)


class TestFindDivisors(unittest.TestCase):
    def test_one(self):
        self.assertEqual(find_divisors(1), {1})

    def test_composite(self):
        self.assertEqual(find_divisors(12), {1, 2, 3, 4, 6, 12})
        self.assertEqual(find_divisors(36), {1, 2, 3, 4, 6, 9, 12, 18, 36})

    def test_prime(self):
        self.assertEqual(find_divisors(13), {1, 13})


class TestFindFactors(unittest.TestCase):
    def test_factors_are_sorted(self):
        self.assertEqual(find_factors(12), [1, 2, 3, 4, 6, 12])
        self.assertEqual(find_factors(36), [1, 2, 3, 4, 6, 9, 12, 18, 36])

    def test_prime_factors_with_multiplicity(self):
        self.assertEqual(prime_factors(120), [2, 2, 2, 3, 5])
        self.assertEqual(prime_factors_duplicate(120), [2, 2, 2, 3, 5])

    def test_prime_factors_of_one(self):
        self.assertEqual(prime_factors(1), [])

    #@unittest.expectedFailure
    def test_prime_factors_of_a_prime(self):
        # Primes below n are sieved, so the remaining prime itself is never emitted.
        self.assertEqual(prime_factors(13), [13])


class TestFindPrimes(unittest.TestCase):
    def test_sieve(self):
        self.assertEqual(find_primes_sieve(10), [2, 3, 5, 7])
        self.assertEqual(
            find_primes_sieve(30),
            [2, 3, 5, 7, 11, 13, 17, 19, 23, 29],
        )

    def test_sieve_small_bounds(self):
        self.assertEqual(find_primes_sieve(2), [])
        self.assertEqual(find_primes_sieve(1), [])

    def test_old_implementation_matches(self):
        self.assertEqual(find_primes_old(30), find_primes_sieve(30))

    def test_prime_check(self):
        self.assertTrue(prime_check(2))
        self.assertTrue(prime_check(3))
        self.assertTrue(prime_check(97))
        self.assertFalse(prime_check(1))
        self.assertFalse(prime_check(4))
        self.assertFalse(prime_check(9))

    def test_zero_is_not_prime(self):
        self.assertFalse(prime_check(0))


class TestLeapYear(unittest.TestCase):
    def test_leap_years(self):
        for year in (2000, 2004, 2024, 1600):
            with self.subTest(year=year):
                self.assertTrue(is_leap(year))

    def test_non_leap_years(self):
        for year in (1900, 2003, 2100, 2023):
            with self.subTest(year=year):
                self.assertFalse(is_leap(year))


class TestLiouvilleFunction(unittest.TestCase):
    def test_known_values(self):
        expected = {1: 1, 2: -1, 4: 1, 6: 1, 8: -1, 30: -1, 120: -1}
        for n, value in expected.items():
            with self.subTest(n=n):
                self.assertEqual(liouville_function(n), value)

    def test_result_is_always_plus_or_minus_one(self):
        for n in range(1, 50):
            with self.subTest(n=n):
                self.assertIn(liouville_function(n), (1, -1))


class TestNNacci(unittest.TestCase):
    def test_documented_example(self):
        self.assertEqual(n_nacci(11, 10), 1)

    def test_reduces_to_n_minus_m_plus_n_minus_m_minus_one(self):
        self.assertEqual(n_nacci(5, 3), 3)
        self.assertEqual(n_nacci(3, 2), 1)

    def test_invalid_parameters(self):
        with self.assertRaises(SystemError):
            n_nacci(1, 2)
        with self.assertRaises(SystemError):
            n_nacci(2, 2)


class TestNaturalNumbers(unittest.TestCase):
    def test_positive_integers(self):
        self.assertTrue(is_natural_num(1))
        self.assertTrue(is_natural_num(100))

    def test_invalid_values(self):
        for value in (0, -1, 1.0, True):
            with self.subTest(value=value):
                self.assertFalse(is_natural_num(value))

    def test_non_comparable_values_raise_type_error(self):
        # The value is compared with 0 before its type is checked,
        # so non-numeric inputs raise instead of returning False.
        for value in ("1", None):
            with self.subTest(value=value):
                with self.assertRaises(TypeError):
                    is_natural_num(value)


class TestPerfectNumber(unittest.TestCase):
    def test_perfect_numbers(self):
        for number in (6, 28, 496):
            with self.subTest(number=number):
                self.assertTrue(perfect_number(number))

    def test_non_perfect_numbers(self):
        for number in (1, 12, 100):
            with self.subTest(number=number):
                self.assertFalse(perfect_number(number))


class TestPerfectSquare(unittest.TestCase):
    def test_squares(self):
        for number in (0, 1, 4, 9, 16, 1000000):
            with self.subTest(number=number):
                self.assertTrue(per_sqr(number))

    def test_non_squares(self):
        for number in (2, 8, 10, 15):
            with self.subTest(number=number):
                self.assertFalse(per_sqr(number))

    def test_negative_input_raises(self):
        with self.assertRaises(ValueError):
            per_sqr(-4)


class TestPermutation(unittest.TestCase):
    def test_known_values(self):
        self.assertEqual(permutations(5, 2), 20)
        self.assertEqual(permutations_(5, 2), 20.0)

    def test_boundaries(self):
        self.assertEqual(permutations(5, 0), 1)
        self.assertEqual(permutations(5, 5), 120)


class TestTotient(unittest.TestCase):
    def test_known_values(self):
        expected = {1: 1, 9: 6, 10: 4, 12: 4}
        for n, value in expected.items():
            with self.subTest(n=n):
                self.assertEqual(totient(n), value)

    #@unittest.expectedFailure
    def test_totient_of_a_prime(self):
        # phi(p) == p - 1; the prime-factor helper returns [] for primes,
        # so the current implementation returns p instead.
        self.assertEqual(totient(13), 12)


if __name__ == "__main__":
    unittest.main()
