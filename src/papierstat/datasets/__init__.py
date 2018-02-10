# -*- coding: utf-8 -*-
"""
@file
@brief Fonctions retournant des jeux de données.
"""
import os
import pickle
from io import StringIO
import pandas
from pyquickhelper.filehelper import unzip_files, get_url_content_timeout


def get_data_folder():
    """
    Retourne le répertoire de données inclus dans ce module.
    """
    this = os.path.dirname(__file__)
    data = os.path.join(this, "data")
    return os.path.abspath(this)


def load_wines_dataset(download=False):
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
        return df
    else:
        fold = get_data_folder()
        data = os.path.join(fold, 'data', 'wines-quality.csv')
        return pandas.read_csv(data)


def load_movielens_dataset(name='small', cache=None, fLOG=None):
    """
    Retourne un jeu de données extrait de la page
    `movielens <https://grouplens.org/datasets/movielens/>`_.

    @param      name    nom du jeu de données à télécharger
    @param      cache   cache les files avec :epkg:`pickle`
    @param      fLOG    logging function
    @return             dictionnaires de dataframes

    *cache* est un fichier, si celui-ci est présent, il recherché
    avec le module :epkg:`pickle`.
    """
    if cache is not None and os.path.exists(cache):
        with open(cache, 'rb') as f:
            return pickle.load(f)
    if name == 'small':
        url = 'http://files.grouplens.org/datasets/movielens/ml-latest-small.zip'
    else:
        raise ValueError("Value '{0}' is not implemented.".format(name))
    if fLOG:
        fLOG("[load_movielens_dataset] download '{0}'".format(url))
    res = get_url_content_timeout(url, encoding=None, fLOG=fLOG)
    if fLOG:
        fLOG("[load_movielens_dataset] unzip {0} bytes".format(len(res)))
    found = unzip_files(res, fLOG=fLOG)
    if fLOG:
        fLOG("[load_movielens_dataset] found {0} files".format(len(found)))
    dfiles = {}
    for name, text in found:
        if name.endswith('.csv'):
            df = pandas.read_csv(StringIO(text.decode('utf-8')), sep=',')
            key = os.path.splitext(os.path.split(name)[-1])[0]
            dfiles[key] = df
    if cache is not None:
        with open(cache, 'wb') as f:
            pickle.dump(dfiles, f)
    return dfiles
