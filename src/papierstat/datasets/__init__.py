# -*- coding: utf-8 -*-
"""
@file
@brief Fonctions retournant des jeux de données.
"""
import os
import pandas


def get_data_folder():
    """
    Retourne le répertoire de données inclut dans ce module.
    """
    this = os.path.dirname(__file__)
    data = os.path.join(this, "data")
    return os.path.abspath(this)


def load_wines_dataset(download=False):
    """
    Retourne le jeu de données
    `wines quality <https://archive.ics.uci.edu/ml/datasets/wine+quality>`_.

    @param  download    télécharge le jeu de données ou considères une copie en local.
    @return             :epkg:`pandas:DataFrame`

    Notebooks associés à ce jeu de données :

    .. runpython::
        :rst:

        from papierstat.datasets.documentation import list_notebooks_rst_links
        links = list_notebooks_rst_links('lectures', 'wines')
        links = ['    * %s' % s for s in links]
        print('\\n'.join(links))
    """
    if download:
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/"
        red = pandas.read_csv(url + "winequality-red.csv", sep=';')
        white = pandas.read_csv(url + "winequality-white.csv", sep=';')
        red['color'] = 'red'
        white['color'] = 'white'
        df = pandas.concat([red, white])
        df.columns = [_.replace(' ', '_') for _ in df.columns]
        return df
    else:
        fold = get_data_folder()
        data = os.path.join(fold, 'data', 'wines-quality.csv')
        return pandas.read_csv(data)
