# -*- coding: utf-8 -*-
"""
@brief      test log(time=20s)
"""

import sys
import os
import unittest
from pyquickhelper.loghelper import fLOG
from pyquickhelper.pycode import add_missing_development_version, skipif_travis, skipif_appveyor
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


class TestNotebookArtificielToken(unittest.TestCase):

    def setUp(self):
        add_missing_development_version(["jyquickhelper"], __file__, hide=True)

    @skipif_travis("ModuleNotFoundError: No module named 'google_compute_engine'")
    @skipif_appveyor("ValueError: 93066 exceeds max_map_len(32768)")
    def test_notebook_artificiel_token(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        import nltk
        nltk.download('punkt')
        nltk.download('stopwords')

        self.assertTrue(src.papierstat is not None)
        folder = os.path.join(os.path.dirname(__file__),
                              "..", "..", "_doc", "notebooks", "lectures")
        test_notebook_execution_coverage(
            __file__, "artificiel_tokenize", folder, 'papierstat', copy_files=[], fLOG=fLOG)


if __name__ == "__main__":
    unittest.main()
