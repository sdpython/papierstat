# -*- coding: utf-8 -*-
"""
@file
@brief Jeux de données reliés aux catégories.
"""
import os
from io import StringIO, BytesIO
import pandas
from pyquickhelper.filehelper import read_content_ufs, ungzip_files
from .data_helper import get_data_folder


def load_adult_dataset(download=True, small=False, url='uci'):
    """
    Retourne le jeu de données
    `Adult Data Set  <https://archive.ics.uci.edu/ml/datasets/adult>`_.
    Notebooks associés à ce jeu de données :

    .. runpython::
        :rst:

        from papierstat.datasets.documentation import list_notebooks_rst_links
        links = list_notebooks_rst_links('lectures', 'adult')
        links = ['    * %s' % s for s in links]
        print('\\n'.join(links))

    @param  download    télécharge le jeu de données ou considères une copie en local.
    @param  small       récupère une version allégée en local
    @param  uci         source
    @return             :epkg:`pandas:DataFrame` (train, test)
    """
    columns = ['age', 'workclass', 'fnlwgt', 'education', 'education_num', 'marital_status',
               'occupation', 'relationship', 'race', 'sex', 'capital_gain', 'capital_loss',
               'hours_per_week', 'native_country', '<=50K']

    if small:
        fold = get_data_folder()
        data_train = os.path.join(fold, 'adult.data.gz')
        data_test = os.path.join(fold, 'adult.test.gz')
        train = pandas.read_csv(data_train, header=None)
        test = pandas.read_csv(data_test, header=None)
        train.columns = columns
        test.columns = columns
    elif download:
        if url == 'uci':
            url = "https://archive.ics.uci.edu/ml/machine-learning-databases/adult/"
            train = pandas.read_csv(url + "adult.data", header=None)
            test = pandas.read_csv(url + "adult.test", header=None, skiprows=1)
        else:
            url = "http://www.xavierdupre.fr/enseignement/complements/"
            tr = read_content_ufs(url + "adult.data.gz",
                                  asbytes=True, encoding=None)
            by = BytesIO(tr)
            tx = ungzip_files(by, unzip=False)
            st = StringIO(tx.decode('ascii'))
            train = pandas.read_csv(st, header=None)
            te = read_content_ufs(url + "adult.test.gz",
                                  asbytes=True, encoding=None)
            by = BytesIO(te)
            tx = ungzip_files(by, unzip=False)
            st = StringIO(tx.decode('ascii'))
            test = pandas.read_csv(st, header=None, skiprows=1)
        train.columns = columns
        test.columns = columns
    else:
        raise NotImplementedError("No local copy")
    label = '<=50K'
    train[label] = train[label].str.strip(' .')
    test[label] = test[label].str.strip(' .')
    cols = train.select_dtypes(object).columns
    for c in cols:
        train[c] = train[c].str.strip()
    for c in cols:
        test[c] = test[c].str.strip()
    return train, test
