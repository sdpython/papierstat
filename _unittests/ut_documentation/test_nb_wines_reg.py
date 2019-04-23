# -*- coding: utf-8 -*-
"""
@brief      test log(time=64s)
"""
import os
import unittest
from pyquickhelper.loghelper import fLOG
from pyquickhelper.pycode import add_missing_development_version, skipif_circleci
from pyquickhelper.ipythonhelper import test_notebook_execution_coverage
import papierstat


class TestNotebookWinesReg(unittest.TestCase):

    def setUp(self):
        add_missing_development_version(["jyquickhelper"], __file__, hide=True)

    @skipif_circleci('timeout')
    def test_notebook_wines_reg(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        self.assertTrue(papierstat is not None)
        folder = os.path.join(os.path.dirname(__file__),
                              "..", "..", "_doc", "notebooks", "lectures")
        test_notebook_execution_coverage(
            __file__, "wines_reg", folder, 'papierstat', copy_files=[], fLOG=fLOG,
            filter_name=lambda n: '_poly' not in n)


if __name__ == "__main__":
    unittest.main()
