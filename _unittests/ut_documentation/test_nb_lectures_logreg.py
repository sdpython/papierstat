# -*- coding: utf-8 -*-
"""
@brief      test log(time=9s)
"""

import sys
import os
import unittest
from pyquickhelper.loghelper import fLOG
from pyquickhelper.pycode import add_missing_development_version
from pyquickhelper.ipythonhelper import test_notebook_execution_coverage


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

import src.papierstat


class TestNotebookLecturesLogReg(unittest.TestCase):

    def setUp(self):
        add_missing_development_version(["jyquickhelper"], __file__, hide=True)

    def test_notebook_lectures_linreg(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        self.assertTrue(src.papierstat is not None)
        folder = os.path.join(os.path.dirname(__file__),
                              "..", "..", "_doc", "notebooks", "lectures")
        test_notebook_execution_coverage(
            __file__, "logreg", folder, 'papierstat', copy_files=[], fLOG=fLOG,
            filter_name=lambda n: "" in n)


if __name__ == "__main__":
    unittest.main()