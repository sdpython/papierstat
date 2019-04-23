# -*- coding: utf-8 -*-
"""
@brief      test log(time=10s)
"""
import os
import unittest
from pyquickhelper.loghelper import fLOG
from pyquickhelper.pycode import add_missing_development_version, skipif_travis
from pyquickhelper.ipythonhelper import test_notebook_execution_coverage
import papierstat


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
        self.assertTrue(papierstat is not None)
        folder = os.path.join(os.path.dirname(__file__),
                              "..", "..", "_doc", "notebooks", "visualisation")
        test_notebook_execution_coverage(
            __file__, "enedis_cartes_bokeh", folder, 'papierstat', copy_files=[], fLOG=fLOG,
            modules=[pyensae])


if __name__ == "__main__":
    unittest.main()
