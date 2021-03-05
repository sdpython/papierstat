
Machine Learning non supervisé
==============================

.. contents::
    :local:

Réduction de dimension
++++++++++++++++++++++

L'`Analyse en Composantes Principales <https://fr.wikipedia.org/wiki/Analyse_en_composantes_principales>`_
est le procédé le plus connu pour réduire les dimensions.
Supposons qu'on doive résoudre un problème de régression
:math:`y=f(X)+\epsilon` où :math:`X=(x_1,...,x_n)`
contient *n* variables. Réduire les dimensions consiste
à construire :math:`m < n` variables fonctions
des premières dont on se sert ensuite pour construire
la régression : :math:`y = f(p(X)) + \epsilon`.
On s'en sert pour deux raisons :

* Avoir une fonction *f* plus simple puisque moins de variables,
* Construire d'autres variables :math:`p(X)` moins bruitées,
  donc plus performantes.

Une façon de construire *p* consiste à minimiser la
perte d'information : :math:`\norme{p^{-1}(p(X)) - X}`.
La fonction *p* linéaire correspond à l'analyse
en composantes principales.

Clustering
++++++++++

L'algorithme le plus connu est un des plus simples
est l'alogorithme des centres mobiles ou
`k-means <http://www.xavierdupre.fr/app/mlstatpy/helpsphinx/c_clus/kmeans.html>`_.
Il suppose que les points appartiennent à un espace vectoriel donc on
peut calculer un barycentre.

Il n'est pas toujours possible de calculer un barycentre,
l'espace considéré n'est pas vectoriel, juste métrique :
il existe une distance.
Le tableau `clustering <http://scikit-learn.org/stable/modules/clustering.html>`_
liste de nombreuses options ainsi que les hypothèses faites sur les points
à clusteriser.

Selon la nature des données, on peut penser aussi à des méthodes comme
`Latent Dirichlet Allocation <http://scikit-learn.org/stable/modules/generated/sklearn.decomposition.LatentDirichletAllocation.html#sklearn.decomposition.LatentDirichletAllocation.transform>`_.

La suite est un exemple d'utilisation de ce type d'algorithme :
`City bike in Chicago <http://www.xavierdupre.fr/app/ensae_projects/helpsphinx/challenges/city_bike.html>`_.

Exercice
++++++++

Le notebook suivant se propose de d'étudier le comportement
des cyclistes dans la ville de Chicago et d'en déduire leurs
habitudes à l'aide d'une méthode de clustering :
`Clustering <http://www.xavierdupre.fr/app/ensae_teaching_cs/helpsphinx/notebooks/td2a_clustering.html>`_.

.. toctree::
    :maxdepth: 1

    ../notebooks/constraint_kmeans
