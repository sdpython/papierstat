# -*- coding: utf-8 -*-
"""
@brief      test log(time=98s)
"""
import unittest
from pyquickhelper.pycode import ExtTestCase
from papierstat.datasets import load_biased


class TestBiased(ExtTestCase):

    def test_load_biased(self):
        train, test = load_biased()
        self.assertEqual(train.shape, (187, 4))
        self.assertEqual(test.shape, (63, 4))
        self.assertEqual(set(train['gender']), {0, 1})
        self.assertGreater(min(train['age']), 18)
        self.assertLess(max(train['age']), 66)
        self.assertGreater(min(train['R']), 1000)
        self.assertLess(max(train['R']), 3001)


if __name__ == "__main__":
    unittest.main()
