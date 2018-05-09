# -*- coding: utf-8 -*-
"""
@brief      test log(time=24s)
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


class TestNotebookVisualisationCarreau(unittest.TestCase):

    def setUp(self):
        add_missing_development_version(
            ["jyquickhelper", "pyensae"], __file__, hide=True)

    def test_notebook_visualisation_carreau(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        import pyensae
        self.assertTrue(src.papierstat is not None)
        folder = os.path.join(os.path.dirname(__file__),
                              "..", "..", "_doc", "notebooks", "visualisation")
        test_notebook_execution_coverage(
            __file__, "carreau", folder, 'papierstat', copy_files=[], fLOG=fLOG,
            modules=[pyensae])


if __name__ == "__main__":
    unittest.main()
