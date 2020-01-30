# -*- coding: utf-8 -*-
"""
@brief      test log(time=65s)
"""
import os
import unittest
from pyquickhelper.loghelper import fLOG
from pyquickhelper.pycode import add_missing_development_version
from pyquickhelper.ipythonhelper import test_notebook_execution_coverage
import papierstat


class TestNotebookEnCoursWines2019(unittest.TestCase):

    def setUp(self):
        add_missing_development_version(["jyquickhelper"], __file__, hide=True)

    def test_notebook_encours_wines_2019(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        self.assertTrue(papierstat is not None)
        folder = os.path.join(os.path.dirname(__file__),
                              "..", "..", "_doc", "notebooks", "encours")
        test_notebook_execution_coverage(
            __file__, "2019", folder, 'papierstat', copy_files=[], fLOG=fLOG,
            filter_name=lambda n: "2019" in n)


if __name__ == "__main__":
    unittest.main()
