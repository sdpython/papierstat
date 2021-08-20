# -*- coding: utf-8 -*-
"""
@brief      test log(time=13s)
"""
import unittest
from bokeh.models import GeoJSONDataSource
from pyquickhelper.pycode import ExtTestCase
from papierstat.datasets import get_geojson_countries


class TestGeoJSON(ExtTestCase):

    def test_geojson(self):
        name = get_geojson_countries()
        self.assertExists(name)
        with open(name, 'r') as f:  # pylint: disable=W1514
            geo = GeoJSONDataSource(geojson=f.read())
        self.assertTrue(geo is not None)


if __name__ == "__main__":
    unittest.main()
