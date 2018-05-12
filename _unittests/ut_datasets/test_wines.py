# -*- coding: utf-8 -*-
"""
@brief      test log(time=13s)
"""

import sys
import os
import unittest
from pyquickhelper.loghelper import fLOG
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

from src.papierstat.datasets import load_wines_dataset


class TestWines(ExtTestCase):

    def test_wines_download(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        df = load_wines_dataset(download=True)
        self.assertEqual(df.shape, (6497, 13))

    def test_wines_local(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        df = load_wines_dataset(download=False)
        self.assertEqual(df.shape, (6497, 13))


if __name__ == "__main__":
    unittest.main()
