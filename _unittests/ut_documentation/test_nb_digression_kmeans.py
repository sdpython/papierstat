# -*- coding: utf-8 -*-
"""
@brief      test log(time=12s)
"""
import os
import unittest
from pyquickhelper.loghelper import fLOG
from pyquickhelper.pycode import add_missing_development_version
from pyquickhelper.ipythonhelper import test_notebook_execution_coverage
import papierstat


class TestNotebookDigressionKMeans(unittest.TestCase):

    def setUp(self):
        add_missing_development_version(["jyquickhelper"], __file__, hide=True)

    def test_notebook_digression_kmeans(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        self.assertTrue(papierstat is not None)
        folder = os.path.join(os.path.dirname(__file__),
                              "..", "..", "_doc", "notebooks", "digressions")
        test_notebook_execution_coverage(
            __file__, "kmeans", folder, 'papierstat', copy_files=[], fLOG=fLOG,
            filter_name=lambda n: "" in n)


if __name__ == "__main__":
    unittest.main()
