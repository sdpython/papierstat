# -*- coding: utf-8 -*-
"""
@brief      test log(time=13s)
"""

import sys
import os
import unittest
from bokeh.models import GeoJSONDataSource
from pyquickhelper.loghelper import fLOG
from pyquickhelper.pycode import ExtTestCase

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

from src.papierstat.datasets import get_geojson_countries


class TestGeoJSON(ExtTestCase):

    def test_geojson(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        name = get_geojson_countries()
        self.assertExists(name)
        with open(name, 'r') as f:
            geo = GeoJSONDataSource(geojson=f.read())
        self.assertTrue(geo is not None)


if __name__ == "__main__":
    unittest.main()
