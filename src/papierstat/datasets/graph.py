# -*- coding: utf-8 -*-
"""
@file
@brief Fonctions retournant des jeux de données liés aux graphes.
"""
import numpy


def create_tiny_graph():
    """
    Graphe très petit. La fonction retourne une matrice
    dans laquelle chaque élément représente la probabilité
    de passer du noeud *i* au noeud *j*.
    Notebooks associés à ce jeu de données :

    @return     matrice

    .. runpython::
        :rst:

        from papierstat.datasets.documentation import list_notebooks_rst_links
        links = list_notebooks_rst_links('lectures', 'tinygraph')
        links = ['    * %s' % s for s in links]
        print('\\n'.join(links))

    @return             :epkg:`pandas:DataFrame`

    .. runpython::
        :showcode:

        from papierstat.datasets import create_tiny_graph
        print(create_tiny_graph())

    .. plot::

        import networkx as nx
        G = nx.Graph()
        for i in range(0, max(P.shape)):
            G.add_node(i)
        for i in range(0, P.shape[0]):
            for j in range(0, P.shape[1]):
                if P[i,j] !=0 :
                    G.add_edge(i,j, weight=int(P[i,j] * 100)/100)

        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(1, 1, figsize=(3,3))
        pos = nx.shell_layout(G)
        nx.draw(G, with_labels=True, font_weight='bold', ax=ax, pos=pos)
        nx.draw_networkx_edge_labels(G, pos=pos)
        plt.show()
    """
    r3 = 1. / 3
    P = numpy.matrix([[0, 0.5, 0, 0.5], [0.5, 0, 0.5, 0],
                      [r3, r3, 0, r3], [0.1, 0.9, 0, 0]])
    return P
