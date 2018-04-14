# -*- coding: utf-8 -*-
"""
@brief      test log(time=13s)
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
from pyquickhelper.pycode import ExtTestCase
from src.papierstat.datasets.documentation import list_notebooks_rst_links


class TestDocumentation(ExtTestCase):

    def test_documentation_wines(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        links = list_notebooks_rst_links('lectures', 'wines')
        self.assertNotEmpty(links)
        self.assertEndsWith("rst`", links[0])
        self.assertStartsWith(':ref:`wines', links[0])

    def test_documentation_movie(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        links = list_notebooks_rst_links('lectures', 'movielens')
        self.assertNotEmpty(links)
        self.assertEndsWith("rst`", links[0])
        self.assertStartsWith(':ref:`movielens', links[0])
        self.assertLesser(len(links), 5)


if __name__ == "__main__":
    unittest.main()
