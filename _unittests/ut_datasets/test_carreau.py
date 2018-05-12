# -*- coding: utf-8 -*-
"""
@brief      test log(time=13s)
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

from src.papierstat.datasets import load_carreau_from_zip


class TestCarreau(ExtTestCase):

    def test_carreau_reunion(self):
        dfcar, shpcar, dfrect, shprect = load_carreau_from_zip()
        self.assertEqual(dfcar.shape, (14076, 5))
        self.assertEqual(dfrect.shape, (7342, 25))
        self.assertEqual(shpcar.shape, (14076, 3))
        self.assertEqual(shprect.shape, (7342, 2))
        self.assertEqual(shpcar.iloc[0, 0], "CRS2975RES200mN7634200E0359400")
        self.assertEqual(shpcar.iloc[0, 1], "UTM40S200M_N38171E01797")
        self.assertEqual(shprect.iloc[0, 0], "N38171E01797-N38172E01797")


if __name__ == "__main__":
    unittest.main()
