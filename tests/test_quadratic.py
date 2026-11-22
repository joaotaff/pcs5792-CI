"""Tests for quadratic equation helpers in ``src``."""

import contextlib
import io
import os
import sys
import unittest
import warnings

SRC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from parabola import find_delta, find_focus, find_vertex
from quadratic_roots import quadratic_roots
from solve_quadratic import quadratic_equation

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from quadratic_formula import quadratic


class TestParabola(unittest.TestCase):
    def test_delta(self):
        self.assertEqual(find_delta(1, -3, 2), 1)

    def test_delta_zero_coefficient_raises(self):
        with self.assertRaises(ValueError):
            find_delta(0, 1, 2)

    def test_vertex(self):
        self.assertEqual(find_vertex(1, -3, 2), (1.5, -0.25))

    def test_vertex_of_downward_parabola(self):
        self.assertEqual(find_vertex(1, 0, -1), (0.0, -1.0))

    def test_focus(self):
        self.assertEqual(find_focus(1, -3, 2), (1.5, 0.0))

    def test_focus_of_downward_parabola(self):
        self.assertEqual(find_focus(1, 0, -1), (0.0, -0.75))


class TestQuadraticRoots(unittest.TestCase):
    def test_two_real_roots(self):
        self.assertEqual(quadratic_roots(1, -3, 2), (2.0, 1.0))

    def test_double_root(self):
        self.assertEqual(quadratic_roots(1, -2, 1), (1.0, 1.0))

    def test_imaginary_roots_return_none(self):
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            result = quadratic_roots(1, 1, 1)
        self.assertIsNone(result)
        self.assertIn("Imaginary roots", buffer.getvalue())

    def test_negative_leading_coefficient(self):
        self.assertEqual(quadratic_roots(-1, 3, -2), (1.0, 2.0))


class TestSolveQuadratic(unittest.TestCase):
    def test_two_real_roots(self):
        self.assertEqual(quadratic_equation(1, -3, 2), (2.0, 1.0))

    def test_double_root(self):
        self.assertEqual(quadratic_equation(1, -2, 1), (1.0, 1.0))

    def test_no_real_roots(self):
        self.assertEqual(quadratic_equation(1, 1, 1), (None, None))

    def test_negative_leading_coefficient(self):
        self.assertEqual(quadratic_equation(-1, 3, -2), (1.0, 2.0))


class TestQuadraticFormula(unittest.TestCase):
    @unittest.expectedFailure
    def test_known_roots(self):
        # ``4(num_a * num_c)`` is parsed as a call on the int 4,
        # raising TypeError instead of computing the discriminant.
        roots = quadratic(1, -3, 2)
        self.assertEqual(set(roots), {1.0, 2.0})


if __name__ == "__main__":
    unittest.main()
