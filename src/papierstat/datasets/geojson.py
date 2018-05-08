# -*- coding: utf-8 -*-
"""
@file
@brief Jeux de données reliés aux vins.
"""

import os
from .data_helper import get_data_folder


def get_geojson_countries():
    """
    Retourne les contours des pays au format :epkg:`GeoJSON`.
    Les données sont disponibles dans le répertoire
    `data <https://github.com/sdpython/papierstat/tree/master/src/papierstat/datasets/data>`_
    et viennent de `countries.geo.json <https://github.com/johan/world.geo.json/blob/master/countries.geo.json>`_.
    Notebooks associés à ce jeu de données :

    .. runpython::
        :rst:

        from papierstat.datasets.documentation import list_notebooks_rst_links
        links = list_notebooks_rst_links('visualisation', 'enedis_cartes')
        links = ['    * %s' % s for s in links]
        print('\\n'.join(links))

    @param          cache       where to cache or unzip the data if downloaded a second time
    @return                     text content (str)
    """
    data = get_data_folder()
    name = os.path.join(data, 'countries.geo.json')
    return name
