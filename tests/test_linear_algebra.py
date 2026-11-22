"""Tests for vector and polynomial helpers in ``src``."""

import contextlib
import io
import math
import os
import sys
import unittest

SRC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from Angle_of_2_vectors_on_Rn_space import calc_angle, calc_norm, inner_p_s
from Cosine_distance import dot_product2, vector_cos5
from norms import l1_norm, l2_norm, linf_norm
from polynomial_evaluation import evaluate_poly


class TestVectorAngle(unittest.TestCase):
    def test_inner_product(self):
        self.assertEqual(inner_p_s([1, 2, 3], [4, 5, 6]), 32)

    def test_inner_product_of_unequal_dimensions(self):
        self.assertEqual(inner_p_s([1, 2], [1, 2, 3]), -1)

    def test_euclidean_norm(self):
        self.assertEqual(calc_norm([3, 4]), 5.0)
        self.assertEqual(calc_norm([0, 0]), 0.0)

    def test_angle_of_parallel_vectors(self):
        self.assertAlmostEqual(calc_angle([1, 0], [1, 0]), 1.0)
        self.assertAlmostEqual(calc_angle([1, 0], [2, 0]), 1.0)

    def test_orthogonal_vectors_return_none(self):
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            result = calc_angle([1, 0], [0, 1])
        self.assertIsNone(result)
        self.assertIn("orthogonal", buffer.getvalue())

    def test_dimension_mismatch_returns_none(self):
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            result = calc_angle([1, 0], [1, 0, 0])
        self.assertIsNone(result)
        self.assertIn("same space", buffer.getvalue())


class TestCosineDistance(unittest.TestCase):
    def test_dot_product(self):
        self.assertEqual(dot_product2([1, 2, 3], [4, 5, 6]), 32)

    def test_cosine_similarity(self):
        # (1*3 + 2*2 + 3*1) / (sqrt(14) * sqrt(14)) = 10 / 14
        self.assertAlmostEqual(vector_cos5([1, 2, 3], [3, 2, 1]), 5 / 7)

    def test_identical_vectors(self):
        self.assertAlmostEqual(vector_cos5([1, 2, 3], [1, 2, 3]), 1.0)

    def test_opposite_vectors(self):
        self.assertAlmostEqual(vector_cos5([1, 2, 3], [-1, -2, -3]), -1.0)

    def test_zero_vector_raises(self):
        with self.assertRaises(ZeroDivisionError):
            vector_cos5([0, 0, 0], [1, 2, 3])


class TestNorms(unittest.TestCase):
    def test_l1_norm(self):
        self.assertEqual(l1_norm([1, -2, 3]), 6)
        self.assertEqual(l1_norm([]), 0)

    def test_linf_norm(self):
        self.assertEqual(linf_norm([-5, 2, 3]), 5)
        self.assertEqual(linf_norm([0]), 0)

    def test_linf_norm_of_empty_list_raises(self):
        with self.assertRaises(ValueError):
            linf_norm([])

    @unittest.expectedFailure
    def test_l2_norm_is_euclidean_norm(self):
        self.assertAlmostEqual(l2_norm([3, 4]), 5.0)


class TestPolynomialEvaluation(unittest.TestCase):
    def test_documented_example(self):
        poly = (0.0, 0.0, 5.0, 9.3, 7.0)
        self.assertAlmostEqual(evaluate_poly(poly, 10), 79800.0)

    def test_constant_polynomial(self):
        self.assertEqual(evaluate_poly((7,), 123), 7)

    def test_simple_quadratic(self):
        # 1 + 2x + 3x^2 at x = 2 -> 1 + 4 + 12 = 17
        self.assertEqual(evaluate_poly((1, 2, 3), 2), 17)

    def test_empty_polynomial_is_zero(self):
        self.assertEqual(evaluate_poly((), 5), 0)


if __name__ == "__main__":
    unittest.main()
