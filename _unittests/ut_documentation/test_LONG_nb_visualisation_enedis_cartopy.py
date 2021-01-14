# -*- coding: utf-8 -*-
"""
@brief      test log(time=24s)
"""
import os
import unittest
from pyquickhelper.loghelper import fLOG
from pyquickhelper.pycode import add_missing_development_version
from pyquickhelper.ipythonhelper import test_notebook_execution_coverage
import papierstat


class TestNotebookVisualisationEnedis(unittest.TestCase):

    def setUp(self):
        add_missing_development_version(
            ["jyquickhelper", "pyensae"], __file__, hide=True)

    def test_notebook_visualisation_enedis(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        import pyensae
        self.assertTrue(papierstat is not None)
        folder = os.path.join(os.path.dirname(__file__),
                              "..", "..", "_doc", "notebooks", "visualisation")
        test_notebook_execution_coverage(
            __file__, "enedis", folder, 'papierstat', copy_files=[], fLOG=fLOG,
            modules=[pyensae], filter_name=lambda n: 'bokeh' not in n)


if __name__ == "__main__":
    unittest.main()
