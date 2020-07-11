# -*- coding: utf-8 -*-
"""
@file
@brief Jeux de données reliés à :epkg:`Enedis`.
"""
import pandas


def load_enedis_dataset(dest='.', fLOG=None):
    """
    Retourne des données extraites du site :epkg:`Enedis` :
    `Production électrique annuelle par filière à la maille commune
    <https://data.enedis.fr/explore/dataset/production-electrique-par-filiere-a-la-maille-commune/export/>`_.
    Le jeu proposé est un extrait pour les années 2015-2016.
    Le téléchargement utilise le module :epkg:`pyensae`.
    Notebooks associés à ce jeu de données :

    .. runpython::
        :rst:

        from papierstat.datasets.documentation import list_notebooks_rst_links
        links = list_notebooks_rst_links('visualisation', 'enedis')
        links = ['    * %s' % s for s in links]
        print('\\n'.join(links))

    @param      dest    répertoire de destination
    @param      fLOG    fonction de log
    @return             :epkg:`pandas:DataFrame`
    """
    from pyensae.datasource import download_data
    name = "production-electrique-par-filiere-a-la-maille-commune.extrait.2015-2016.csv.zip"
    if fLOG:
        res = download_data(name, whereTo=dest, fLOG=fLOG)
    else:
        res = download_data(name, whereTo=dest)
    if len(res) != 1:
        raise ValueError(  # pragma: no cover
            "Unzipping '{0}' failed.".format(name))
    df = pandas.read_csv(res[0], sep=';', encoding='utf-8')
    df['long'] = df['Geo Point 2D'].apply(
        lambda x: float(x.split(',')[1].strip()))
    df['lat'] = df['Geo Point 2D'].apply(
        lambda x: float(x.split(',')[0].strip()))
    return df
