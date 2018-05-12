# -*- coding: utf-8 -*-
"""
@brief      test log(time=10s)
"""

import sys
import os
import unittest
from pyquickhelper.loghelper import fLOG
from pyquickhelper.pycode import add_missing_development_version, skipif_travis
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


class TestNotebookVisualisationEnedisBokeh(unittest.TestCase):

    def setUp(self):
        add_missing_development_version(
            ["jyquickhelper", "pyensae"], __file__, hide=True)

    @skipif_travis('bokeh waiting for too long.')
    def test_notebook_visualisation_enedis_bokeh(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        import pyensae
        self.assertTrue(src.papierstat is not None)
        folder = os.path.join(os.path.dirname(__file__),
                              "..", "..", "_doc", "notebooks", "visualisation")
        test_notebook_execution_coverage(
            __file__, "enedis_cartes_bokeh", folder, 'papierstat', copy_files=[], fLOG=fLOG,
            modules=[pyensae])


if __name__ == "__main__":
    unittest.main()
