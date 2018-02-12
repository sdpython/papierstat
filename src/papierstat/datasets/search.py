# -*- coding: utf-8 -*-
"""
@file
@brief Jeux de données reliés aux vins.
"""
import os
from sklearn.datasets import load_svmlight_file
from .data_helper import get_data_folder


def load_search_engine_dataset(train_or_test=True):
    """
    Retourne un très petit échantillon tiré de
    `Microsoft Learning to Rank Datasets <https://www.microsoft.com/en-us/research/project/mslr/?from=http%3A%2F%2Fresearch.microsoft.com%2Fen-us%2Fprojects%2Fmslr%2F>`_.
    Vu le nombre de features, le petit nombre de requêtes, il est impossible
    d'apprendre un bon modèle, cela permet néanmoins de tester son code.
    La fonction retourne les features d'abord puis les labels.
    Notebooks associés à ce jeu de données :

    .. runpython::
        :rst:

        from papierstat.datasets.documentation import list_notebooks_rst_links
        links = list_notebooks_rst_links('lectures', 'search')
        links = ['    * %s' % s for s in links]
        print('\\n'.join(links))

    @param      train_or_test   True for train, False for test
    @return                     :epkg:`numpy:csr_matrix`, :epkg:`numpy:array`

    La fonction utilise `load_svmlight_file <http://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_svmlight_file.html>`_
    pour lire le fichier. Cette option ne permet l'ouverture de gros fichiers,
    en particulier façon streaming.
    """
    fold = get_data_folder()
    if train_or_test:
        data = os.path.join(fold, 'search_tiny_train.txt')
    else:
        data = os.path.join(fold, 'search_tiny_test.txt')
    df = load_svmlight_file(data)
    return df
