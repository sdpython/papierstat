# -*- coding: utf-8 -*-
"""
@file
@brief Jeux de données reliés aux vins.
"""
import os
import pandas


def load_sentiment_dataset(cache="."):
    """
    Retourne un ensemble de phrases en anglais avec
    assorties d'un sentiment positif ou négatif.
    Source :
    `Sentiment Labelled Sentences Data Set <https://archive.ics.uci.edu/ml/datasets/Sentiment+Labelled+Sentences>`_.
    Notebooks associés à ce jeu de données :

    .. runpython::
        :rst:

        from papierstat.datasets.documentation import list_notebooks_rst_links
        links = list_notebooks_rst_links('lectures', 'text_sentiment_wordvec')
        links = ['    * %s' % s for s in links]
        print('\\n'.join(links))

    @param          cache       where to cache or unzip the data if downloaded a second time
    @return                     text content (str)
    """
    from pyensae.datasource import download_data
    # url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00331/"
    name = "sentiment_labelled_sentences.zip"
    res = download_data(name, whereTo=cache)
    if len(res) != 9:
        raise ValueError("Unzipping '{0}' failed.".format(name))
    dfs = []
    for fi in res:
        if ".txt" not in fi or "readme" in fi or "__MACOSX" in fi:
            continue
        df = pandas.read_csv(fi, sep='\t', quoting=3,
                             names=['sentence', 'sentiment'])
        df["source"] = os.path.splitext(os.path.split(fi)[-1])[0]
        dfs.append(df)
    return pandas.concat(dfs)
