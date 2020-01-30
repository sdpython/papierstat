# -*- coding: utf-8 -*-
"""
@brief      test log(time=8s)
"""
import unittest
from pyquickhelper.pycode import ExtTestCase
from papierstat.datasets import load_titanic_dataset


class TestTitanic(ExtTestCase):

    def test_titanic_download(self):
        df = load_titanic_dataset(download=True, subset="A")
        self.assertEqual(df.shape, (1309, 14))
        df = load_titanic_dataset(download=True, subset="B")
        self.assertEqual(df.shape, (1313, 11))

    def test_titanic_local(self):
        df = load_titanic_dataset(download=False, subset="A")
        self.assertEqual(df.shape, (1309, 14))
        df = load_titanic_dataset(download=False, subset="B")
        self.assertEqual(df.shape, (1313, 11))


if __name__ == "__main__":
    unittest.main()
