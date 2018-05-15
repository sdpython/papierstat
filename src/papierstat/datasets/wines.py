# -*- coding: utf-8 -*-
"""
@file
@brief Jeux de données reliés aux vins.
"""
import os
import pandas
from numpy.random import permutation
from .data_helper import get_data_folder


__all__ = ['load_wines_dataset']


def load_wines_dataset(download=False, shuffle=False):
    """
    Retourne le jeu de données
    `wines quality <https://archive.ics.uci.edu/ml/datasets/wine+quality>`_.
    Notebooks associés à ce jeu de données :

    .. runpython::
        :rst:

        from papierstat.datasets.documentation import list_notebooks_rst_links
        links = list_notebooks_rst_links('lectures', 'wines')
        links = ['    * %s' % s for s in links]
        print('\\n'.join(links))

    @param  download    télécharge le jeu de données ou considères une copie en local.
    @param  shuffle     permute aléatoire les données (elles ne le sont pas)
    @return             :epkg:`pandas:DataFrame`
    """
    if download:
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/"
        red = pandas.read_csv(url + "winequality-red.csv", sep=';')
        white = pandas.read_csv(url + "winequality-white.csv", sep=';')
        red['color'] = 'red'
        white['color'] = 'white'
        df = pandas.concat([red, white])
        df.columns = [_.replace(' ', '_') for _ in df.columns]
    else:
        fold = get_data_folder()
        data = os.path.join(fold, 'wines-quality.csv')
        df = pandas.read_csv(data)
    if shuffle:
        df = df.reset_index(drop=True)
        ind = permutation(df.index)
        df = df.iloc[ind, :].reset_index(drop=True)
    return df
