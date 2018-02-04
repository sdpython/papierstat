
=======================
Devinettes et problèmes
=======================

Cette page regroupe quelques questions et problèmes
dont les solutions figurent dans les pages de ce site
intéressante du point de vue d'un data scientiste.

.. contents::
    :depth: 1
    :local:

Mathématiques
=============

.. contents::
    :local:

Corrélations non linéaires
++++++++++++++++++++++++++

Le `coefficient de Pearson <https://en.wikipedia.org/wiki/Pearson_correlation_coefficient>`_
est sans aucun doute le coefficient de corrélation le plus
connu. Le `coefficient de Spearman <https://en.wikipedia.org/wiki/Spearman%27s_rank_correlation_coefficient>`_
mesure la corrélation entre deux variables à partir de leur rang.
Et si on essayait de définir un coefficient de corrélation
non linéaire ? A base d'arbre de décision ? Pas forcémenet symétrique ?

Décorrélation de variables
++++++++++++++++++++++++++

On suppose que les variables :math:`(X_1, ..., X_n)` sont
corrélées avec une matrice variance coveriance égale à :math:`\Sigma`.
Comment construire des variables décorrélées à partir de
:math:`(X_1, ..., X_n)` ?

p-value et intervalle de confiance
++++++++++++++++++++++++++++++++++

L'école anglaise a tendance à préférer les
`p-values <https://en.wikipedia.org/wiki/P-value>`_,
l'école française préfère les
`intervalles de confiance <https://fr.wikipedia.org/wiki/Intervalle_de_confiance>`_.
Ces deux notions sont équivalentes mais connaissez-vous le lien
qui les unit ?

Méthodologie
============

.. contents::
    :local:

Normalisation
+++++++++++++

Le code suivant présente une erreur de méthodologie
qui a souvent peu d'incidence mais qui n'en reste pas moins
problématique.

::

    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y)

    from sklearn.preprocessing import normalize
    X_train_norm = normalize(X_train)
    X_test_norm = normalize(X_test)

Quelle est elle ?
