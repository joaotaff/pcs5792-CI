"""Tests for geometry helpers in ``src``."""

import contextlib
import io
import math
import os
import sys
import unittest

SRC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from bretschneider import bretschneider
from geometry_basic import (
    area_circle,
    area_cylinder,
    area_sphere,
    area_square,
    area_triangle,
    area_triangle_heron,
    perimeter_circle,
    perimeter_square,
    pythagoras,
    volume_cylinder,
    volume_sphere,
)
from geometry_ellipses import (
    area_ellipse,
    area_surface_ellipsoid,
    circumference_ellipse,
    volume_ellipsoid,
)
from point_distance import multidimensional_distance, point_distance
from slope_line import find_slope


class TestBretschneider(unittest.TestCase):
    def test_unit_square(self):
        # a = b = c = d = 1 with opposite angles of 90 degrees
        self.assertAlmostEqual(bretschneider(1, 1, 1, 1, 90, 90), 1.0, places=5)

    def test_rectangle(self):
        # 2 x 3 rectangle, again with opposite right angles
        self.assertAlmostEqual(bretschneider(2, 3, 2, 3, 90, 90), 6.0, places=5)


class TestGeometryBasic(unittest.TestCase):
    def test_square(self):
        self.assertEqual(area_square(4), 16)
        self.assertEqual(perimeter_square(4), 16)

    def test_triangle_heron(self):
        self.assertAlmostEqual(area_triangle_heron(3, 4, 5), 6.0)

    def test_triangle_base_times_height(self):
        self.assertEqual(area_triangle(10, 5), 25)

    def test_pythagoras(self):
        self.assertAlmostEqual(pythagoras(3, 4), 5.0)

    def test_pythagoras_with_zero_returns_none(self):
        self.assertIsNone(pythagoras(0, 0))

    def test_circle(self):
        self.assertAlmostEqual(area_circle(1), math.pi)
        self.assertAlmostEqual(perimeter_circle(1), 2 * math.pi)

    def test_sphere(self):
        self.assertAlmostEqual(volume_sphere(1), 4 / 3 * math.pi)
        self.assertAlmostEqual(area_sphere(1), 4 * math.pi)

    def test_cylinder(self):
        self.assertAlmostEqual(area_cylinder(1, 2), 6 * math.pi)
        self.assertAlmostEqual(volume_cylinder(1, 2), 2 * math.pi)


class TestGeometryEllipses(unittest.TestCase):
    def test_ellipsoid_volume(self):
        self.assertAlmostEqual(volume_ellipsoid(1, 1, 1), 4 / 3 * math.pi)
        self.assertAlmostEqual(volume_ellipsoid(3, 2, 1), 8 * math.pi)

    def test_ellipsoid_surface_area_of_unit_sphere(self):
        self.assertAlmostEqual(area_surface_ellipsoid(1, 1, 1), 4 * math.pi)

    def test_ellipse_area(self):
        self.assertAlmostEqual(area_ellipse(2, 3), 6 * math.pi)

    def test_circle_as_special_ellipse(self):
        self.assertAlmostEqual(circumference_ellipse(3, 3), 6 * math.pi)


class TestPointDistance(unittest.TestCase):
    def test_two_dimensional_distance(self):
        self.assertAlmostEqual(point_distance((0, 0), (3, 4)), 5.0)

    def test_symmetric(self):
        self.assertAlmostEqual(
            point_distance((1, 2), (4, 6)),
            point_distance((4, 6), (1, 2)),
        )

    def test_same_point(self):
        self.assertEqual(point_distance((2, 2), (2, 2)), 0.0)

    def test_multidimensional_distance(self):
        self.assertAlmostEqual(multidimensional_distance((1, 2, 2), (0, 0, 0)), 3.0)

    def test_dimension_mismatch_returns_none_and_warns(self):
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            result = multidimensional_distance((1, 2), (1, 2, 3))
        self.assertIsNone(result)
        self.assertEqual(buffer.getvalue(), "Points of unequal dimensions\n")


class TestSlopeLine(unittest.TestCase):
    def test_slope(self):
        self.assertAlmostEqual(find_slope((0, 0), (2, 4)), 2.0)

    def test_horizontal_line(self):
        self.assertEqual(find_slope((1, 3), (5, 3)), 0.0)

    def test_negative_slope(self):
        self.assertAlmostEqual(find_slope((0, 4), (2, 0)), -2.0)

    def test_vertical_line_raises(self):
        with self.assertRaises(ZeroDivisionError):
            find_slope((1, 0), (1, 5))


if __name__ == "__main__":
    unittest.main()
