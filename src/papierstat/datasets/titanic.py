# -*- coding: utf-8 -*-
"""
@file
@brief Jeux de données reliés aux vins.
"""
import os
import pandas
from .data_helper import get_data_folder


__all__ = ['load_titanic_dataset']


def load_titanic_dataset(download=False, subset="A"):
    """
    Retourne le jeu de données Titanic,
    Data obtained from `biostat.mc.vanderbilt.edu/DataSets
    <http://biostat.mc.vanderbilt.edu/DataSets>`_.
    Notebooks associés à ce jeu de données :

    .. runpython::
        :rst:

        from papierstat.datasets.documentation import list_notebooks_rst_links
        links = list_notebooks_rst_links('encours', contains='titanic')
        links = ['    * %s' % s for s in links]
        print('\\n'.join(links))

    @param  download    télécharge le jeu de données ou considères une copie en local.
    @param  subset      ``"A"`` ou ``"B"``
    @return             :epkg:`pandas:DataFrame`
    """
    urls = dict(
        A='https://biostat.app.vumc.org/wiki/pub/Main/DataSets/titanic3.csv',
        B='https://biostat.app.vumc.org/wiki/pub/Main/DataSets/titanic.txt'
    )
    url = urls[subset]
    if download:
        df = pandas.read_csv(url)
    else:
        fold = get_data_folder()
        data = os.path.join(fold, url.split('/')[-1])
        df = pandas.read_csv(data)
    return df
