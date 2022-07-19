# -*- coding: utf-8 -*-
"""
@brief      test log(time=3s)
"""
import os
import unittest
import pandas
from pyquickhelper.loghelper import fLOG
from pyquickhelper.pycode import ExtTestCase, get_temp_folder
from papierstat.datasets import load_movielens_dataset


class TestMovieLens(ExtTestCase):

    def test_movielens(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        temp = get_temp_folder(__file__, 'temp_movielens')
        cache = os.path.join(temp, 'cache.pkl')
        dfs = load_movielens_dataset(fLOG=fLOG, cache=cache)
        self.assertIsInstance(dfs, dict)
        nb = 0
        for k, v in dfs.items():
            self.assertIsInstance(v, pandas.DataFrame)
            self.assertGreater(len(v), 0)
            if k == 'ratings':
                self.assertEqual(v.shape[1], 4)
                self.assertGreater(v.shape[0], 100004)
                nb += 1
        self.assertEqual(nb, 1)
        self.assertGreater(len(dfs), 0)
        dfs2 = load_movielens_dataset(fLOG=fLOG, cache=cache)
        for k in dfs2:
            self.assertEqualDataFrame(dfs[k], dfs2[k])
        name = os.path.join(temp, '..', 'ml-latest-small.zip')
        if os.path.exists(name):
            raise Exception(
                f"This file '{name}' should not be present.")


if __name__ == "__main__":
    unittest.main()
