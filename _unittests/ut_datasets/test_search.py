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

from src.papierstat.datasets import load_search_engine_dataset


class TestWines(ExtTestCase):

    def test_wines_download(self):
        x1, y1, qid1 = load_search_engine_dataset(True)
        x2, y2, qid2 = load_search_engine_dataset(False)
        self.assertEqual(x1.shape[1], x2.shape[1])
        self.assertEqual(x1.shape[0], y1.shape[0])
        self.assertEqual(x2.shape[0], y2.shape[0])
        self.assertEqual(x1.shape, (582, 136))
        self.assertEqual(qid1.shape[0], 582)
        self.assertEqual(y1.shape[0], 582)
        self.assertEqual(qid2.shape[0], 403)
        self.assertEqual(y2.shape[0], 403)
        self.assertTrue(set(qid1), {1, 76, 46, 16, 91, 61, 31})


if __name__ == "__main__":
    unittest.main()
