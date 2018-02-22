# -*- coding: utf-8 -*-
"""
@file
@brief Jeux de données reliés aux vins.
"""
import os
import pandas
from pyquickhelper.filehelper import unzip_files
from .data_helper import get_data_folder


def load_tweet_dataset(cache="."):
    """
    Retourne quelques tweets extrait en 2016.
    Les données sont disponibles dans le répertoire
    `data <https://github.com/sdpython/papierstat/tree/master/src/papierstat/datasets/data>`_.
    Notebooks associés à ce jeu de données :

    .. runpython::
        :rst:

        from papierstat.datasets.documentation import list_notebooks_rst_links
        links = list_notebooks_rst_links('lectures', 'artificiel_tokenize_features')
        links = ['    * %s' % s for s in links]
        print('\\n'.join(links))

    @param          cache       where to cache or unzip the data if downloaded a second time
    @return                     text content (str)
    """
    data = get_data_folder()
    name = os.path.join(data, 'tweets_macron_sijetaispresident_201609.zip')
    one = unzip_files(name, where_to=cache)
    return pandas.read_csv(one[0], encoding='utf-8', sep='\t')
