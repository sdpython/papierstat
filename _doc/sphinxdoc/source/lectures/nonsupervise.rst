
Machine Learning non supervisé
==============================

Hors texte.

.. contents::
    :local:

Réduction de dimension
++++++++++++++++++++++

* `Analyse en Composantes Principales <https://fr.wikipedia.org/wiki/Analyse_en_composantes_principales>`_

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
`City bike in Chicago <http://www.xavierdupre.fr/app/ensae_projects/helpsphinx/challenges/city_bike.html>`_

Exercice
++++++++

* `Clustering <http://www.xavierdupre.fr/app/ensae_teaching_cs/helpsphinx3/notebooks/td2a_clustering.html>`_
