# -*- coding: utf-8 -*-
"""
@brief      test log(time=98s)
"""

import sys
import os
import unittest
from pyquickhelper.pycode import ExtTestCase


try:
    import src
except ImportError:
    path = os.path.normpath(
        os.path.abspath(
            os.path.join(
                os.path.split(__file__)[0],
                "..",
                "..")))
    if path not in sys.path:
        sys.path.append(path)
    import src

from src.papierstat.datasets import line2d


class TestDummies(ExtTestCase):

    def test_line2d(self):
        mat = line2d(5)
        self.assertEqual(mat.shape, (5, 2))
        self.assertGreater(mat[:, 0].min(), -0.01)
        self.assertLesser(mat[:, 0].max(), 10.01)


if __name__ == "__main__":
    unittest.main()
