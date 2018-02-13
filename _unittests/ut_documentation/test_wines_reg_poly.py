#-*- coding: utf-8 -*-
"""
@brief      test log(time=8s)
"""

import sys
import os
import unittest


try:
    import pyquickhelper as skip_
except ImportError:
    path = os.path.normpath(
        os.path.abspath(
            os.path.join(
                os.path.split(__file__)[0],
                "..",
                "..",
                "..",
                "pyquickhelper",
                "src")))
    if path not in sys.path:
        sys.path.append(path)
    import pyquickhelper as skip_

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

from pyquickhelper.loghelper import fLOG
from pyquickhelper.pycode import add_missing_development_version
from pyquickhelper.ipythonhelper import test_notebook_execution_coverage
import src.papierstat


class TestNotebookWinesRegPoly(unittest.TestCase):

    def setUp(self):
        add_missing_development_version(["jyquickhelper"], __file__, hide=True)

    def test_notebook_wines_reg_poly(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        self.assertTrue(src.papierstat is not None)
        folder = os.path.join(os.path.dirname(__file__),
                              "..", "..", "_doc", "notebooks", "lectures")
        test_notebook_execution_coverage(
            __file__, "wines_reg_poly", folder, 'papierstat', copy_files=[], fLOG=fLOG)


if __name__ == "__main__":
    unittest.main()
