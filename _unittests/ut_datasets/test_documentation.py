# -*- coding: utf-8 -*-
"""
@brief      test log(time=13s)
"""
import unittest
from pyquickhelper.pycode import ExtTestCase
from papierstat.datasets.documentation import list_notebooks_rst_links


class TestDocumentation(ExtTestCase):

    def test_documentation_wines(self):
        links = list_notebooks_rst_links('lectures', 'wines')
        self.assertNotEmpty(links)
        self.assertEndsWith("rst`", links[0])
        self.assertStartsWith(':ref:`wines', links[0])

    def test_documentation_movie(self):
        links = list_notebooks_rst_links('lectures', 'movielens')
        self.assertNotEmpty(links)
        self.assertEndsWith("rst`", links[0])
        self.assertStartsWith(':ref:`movielens', links[0])
        self.assertLesser(len(links), 5)


if __name__ == "__main__":
    unittest.main()
