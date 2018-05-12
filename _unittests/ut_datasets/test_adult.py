# -*- coding: utf-8 -*-
"""
@brief      test log(time=98s)
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

from src.papierstat.datasets import load_adult_dataset


class TestAdult(ExtTestCase):

    def test_adult_download_uci(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        train, test = load_adult_dataset(download=True)
        self.assertEqual(train.shape, (32561, 15))
        self.assertEqual(test.shape, (16281, 15))

    def test_adult_download_xd(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        train, test = load_adult_dataset(download=True, url='xd')
        self.assertEqual(train.shape, (32561, 15))
        self.assertEqual(test.shape, (16281, 15))

    def test_adult_local(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        train, test = load_adult_dataset(small=True)
        self.assertEqual(train.shape, (11247, 15))
        self.assertEqual(test.shape, (5372, 15))


if __name__ == "__main__":
    unittest.main()
