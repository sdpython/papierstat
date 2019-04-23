# -*- coding: utf-8 -*-
"""
@brief      test log(time=98s)
"""
import unittest
from pyquickhelper.pycode import ExtTestCase
from papierstat.datasets import load_adult_dataset


class TestAdult(ExtTestCase):

    def test_adult_download_uci(self):
        train, test = load_adult_dataset(download=True)
        self.assertEqual(train.shape, (32561, 15))
        self.assertEqual(test.shape, (16281, 15))

    def test_adult_download_xd(self):
        train, test = load_adult_dataset(download=True, url='xd')
        self.assertEqual(train.shape, (32561, 15))
        self.assertEqual(test.shape, (16281, 15))

    def test_adult_local(self):
        train, test = load_adult_dataset(small=True)
        self.assertEqual(train.shape, (11247, 15))
        self.assertEqual(test.shape, (5372, 15))


if __name__ == "__main__":
    unittest.main()
