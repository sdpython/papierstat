# -*- coding: utf-8 -*-
"""
@brief      test log(time=64s)
"""
import os
import unittest
from pyquickhelper.loghelper import fLOG
from pyquickhelper.pycode import add_missing_development_version
from pyquickhelper.ipythonhelper import test_notebook_execution_coverage
import papierstat


class TestNotebookWines(unittest.TestCase):

    def setUp(self):
        add_missing_development_version(["jyquickhelper"], __file__, hide=True)

    def test_notebook_wines(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        self.assertTrue(papierstat is not None)
        folder = os.path.join(os.path.dirname(__file__),
                              "..", "..", "_doc", "notebooks", "lectures")
        test_notebook_execution_coverage(
            __file__, "wines", folder, 'papierstat', copy_files=[], fLOG=fLOG,
            filter_name=lambda n: "wines_reg" not in n)


if __name__ == "__main__":
    unittest.main()
