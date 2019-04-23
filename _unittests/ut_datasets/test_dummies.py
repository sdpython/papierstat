# -*- coding: utf-8 -*-
"""
@brief      test log(time=98s)
"""
import unittest
from pyquickhelper.pycode import ExtTestCase
from papierstat.datasets import line2d


class TestDummies(ExtTestCase):

    def test_line2d(self):
        mat = line2d(5)
        self.assertEqual(mat.shape, (5, 2))
        self.assertGreater(mat[:, 0].min(), -0.01)
        self.assertLesser(mat[:, 0].max(), 10.01)


if __name__ == "__main__":
    unittest.main()
