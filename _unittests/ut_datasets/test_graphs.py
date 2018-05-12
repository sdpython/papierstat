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

from src.papierstat.datasets import create_tiny_graph


class TestGraphs(ExtTestCase):

    def test_create_tiny_graphs(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        P = create_tiny_graph()
        self.assertEqual(P.shape, (4, 4))


if __name__ == "__main__":
    unittest.main()
