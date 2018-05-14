# -*- coding: utf-8 -*-
"""
@file
@brief Jeux de données artificiels.
"""
from numpy.random import rand, randn
from numpy import vstack


def line2d(n, x0=0, x1=10, a=0.5, b=1, sigma=0.5):
    """
    Simule un jeu de données :math:`y = ax + b + \\epsilon`.
    Notebooks associés à ce jeu de données :

    .. runpython::
        :rst:

        from papierstat.datasets.documentation import list_notebooks_rst_links
        links = list_notebooks_rst_links('lectures', 'artificiel_shape')
        links = ['    * %s' % s for s in links]
        print('\\n'.join(links))

    @param          n       nombre de points à simuler
    @param          x0      dans l'intervalle *[x0, x1]*
    @param          x1      dans l'intervalle *[x0, x1]*
    @param          a       *a*
    @param          b       *b*
    @param          sigma   écart type du bruit blanc
    @return                 une matrice
    """
    x = rand(n) * (x1 - x0) + x0
    e = randn(n) * sigma
    y = x * a + b
    y += e
    return vstack([x, y]).T
