.. index:: ranking

.. _l-ranking-section:

Ranking
=======

L'exemple emblématique du ranking est le moteur de recherche
qui cherche des pages internet à partir de mots clés et qui
ordonne selon un ordre de pertinence appris avec une palanquée
de features reliées au contenu, aux clicks, au temps passé
sur la page... Il s'agit d'ordonner un ensemble de résultats
associés à une requête ou plus simplement un identifiant.
Pour résoudre ce problème, on le transforme soit en un problème
de régression où il faut apprendre un score de pertinence,
soit un problème de classification où il faut déterminer
l'ordre de paires de résultats.

.. index:: DCG, NDCG

La première approche est similaire au :ref:`l-collaborative-filtering`.
Le score de pertinence ou rating mesure l'adéquation du résultat
à la requête. Dans le cas d'un moteur de recherche, c'est principalement
cette approche qui est suivie avec comme métrique
le `Discounted Cumulative Gain (DCG) <https://en.wikipedia.org/wiki/Discounted_cumulative_gain>`_
ou sa version normalisée `NDCG <https://en.wikipedia.org/wiki/Discounted_cumulative_gain#Normalized_DCG>`_.

La seconde approche s'inspire de la :ref:`l-multiclass`.
:math:`R=(r_1, ..., r_n)` représente tous les résultats pour
la requête *q*. On apprend un classifieur binaire qui détermine
pour chaque paire de résultat :math:`(r_i, r_j)` lequel
doit être affiché en premier. L'ordre final est déterminé
par le nombre de *matchs* qu'un résultat gagne.

.. toctree::
    :maxdepth: 1

    ../notebooks/search_rank
