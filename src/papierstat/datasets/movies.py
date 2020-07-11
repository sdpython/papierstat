# -*- coding: utf-8 -*-
"""
@file
@brief Jeux de données reliés aux films.
"""
import os
import pickle
from io import StringIO
import pandas
from pyquickhelper.filehelper import unzip_files, get_url_content_timeout


def load_movielens_dataset(name='small', cache=None, fLOG=None):
    """
    Retourne un jeu de données extrait de la page
    `movielens <https://grouplens.org/datasets/movielens/>`_.
    Notebooks associés à ce jeu de données :

    .. runpython::
        :rst:

        from papierstat.datasets.documentation import list_notebooks_rst_links
        links = list_notebooks_rst_links('lectures', 'movielens')
        links = ['    * %s' % s for s in links]
        print('\\n'.join(links))

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
        raise ValueError(  # pragma: no cover
            "Value '{0}' is not implemented.".format(name))
    if fLOG:
        fLOG("[load_movielens_dataset] download '{0}'".format(url))
    res = get_url_content_timeout(url, encoding=None, fLOG=fLOG)
    if fLOG:
        fLOG("[load_movielens_dataset] unzip {0} bytes".format(len(res)))
    found = unzip_files(res, fLOG=fLOG)
    if fLOG:
        fLOG("[load_movielens_dataset] found {0} files".format(len(found)))
    dfiles = {}
    for name_, text in found:
        if name_.endswith('.csv'):
            df = pandas.read_csv(StringIO(text.decode('utf-8')), sep=',')
            key = os.path.splitext(os.path.split(name_)[-1])[0]
            dfiles[key] = df
    if cache is not None:
        with open(cache, 'wb') as f:
            pickle.dump(dfiles, f)
    return dfiles
