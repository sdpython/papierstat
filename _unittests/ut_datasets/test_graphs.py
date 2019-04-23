# -*- coding: utf-8 -*-
"""
@brief      test log(time=13s)
"""
import unittest
from pyquickhelper.pycode import ExtTestCase
from papierstat.datasets import create_tiny_graph


class TestGraphs(ExtTestCase):

    def test_create_tiny_graphs(self):
        P = create_tiny_graph()
        self.assertEqual(P.shape, (4, 4))


if __name__ == "__main__":
    unittest.main()
