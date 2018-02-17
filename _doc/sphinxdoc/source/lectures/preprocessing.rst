
.. _l-preprocessing:

Prétraitement
=============

:epkg:`pandas` est souvent le point d'entrée d'un problème
de machine learning à savoir un fichier plat qu'on lit
avec la fonction :epkg:`pandas:reead_csv`. Lorsqu'on
regarde le code de :epkg:`scikit-learn`, on s'aperçoit que
ces données sont converties dans un tableau :epkg:`numpy`.
Pourquoi ? La réponse tient dans l'image qui suit :

.. image:: images/ml_simple.png
    :width: 250

:epkg:`pandas` sert à préparer les données, à transformer
tout ce qui n'est pas numérique en nombres réelles, à enrichir les données
en fusionnant avec d'autres bases. Une fois que cela est fait, on peut convertir
toutes les données au format numérique, en matrice pour simplfiier car les algorihmes
numériques utilisant principalement cela. Des nombres réels sous forme de matrices,
c'est ce que manipulent tous les algorithmes de machine learning.

.. contents::
    :local:

Prétraitement numériques
++++++++++++++++++++++++

Normalisation, changement d'échelle, passage au logarithme,
suppression des valeurs extrêmes, construction de features
polynômiales, :epkg:`scikit-learn` donne une idée des prétraitements
numériques les plus courants :
`sklearn.preprocessing <http://scikit-learn.org/stable/modules/classes.html#module-sklearn.preprocessing>`_.

Texte - catégorie
+++++++++++++++++

Le texte est rarement exploitable tel quel, il faut le convertir
au format numérique. On peut traiter l'information d'un seul bloc :
chaque valeur est distincte, il s'agit d'une catégorie. Le traitement
le plus simple consiste à convertir chaque valeur en une valeur numérique.
Les variations apparaissent car il faut tenir de la façon dont le modèle
de machine learning est appris (gradient ou méthode ensembliste), et
du nombre de catégories : il y en a trop parfois.

* conversion en entier
* une dimension par catégories
* variations
* hash

Texte - séquence
++++++++++++++++

L'information peut aussi un texte libre qu'on peut découper
soit en mots ou en caractères.

* n-grams
* tf-idf
* bag of words
* embedding avec deep learning

Traitement des valeurs manquantes
+++++++++++++++++++++++++++++++++

Overfitting et distribution des observations
++++++++++++++++++++++++++++++++++++++++++++

smote

.. index:: transformer

Pipeline
++++++++

Les bons vins sont rares
++++++++++++++++++++++++
