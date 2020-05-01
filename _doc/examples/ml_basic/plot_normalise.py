# -*- coding: utf-8 -*-
"""
Normalisation
=============

Quelques lignes pour normaliser.
La page `preprocessing
<https://scikit-learn.org/stable/modules/preprocessing.html>`_
recense tous les prétraitements que la librairie
:epkg:`scikit-learn` implémente.


.. contents::
    :local:
"""

#########################################
# Un jeu de données

from papierstat.datasets import load_wines_dataset
df = load_wines_dataset()
X = df.drop(['quality', 'color'], axis=1)
y = df['quality']

print(X.head())

#########################################
# Normalisation naïve
# -------------------
from sklearn.preprocessing import normalize
X_norm = normalize(X)
print(X_norm[:5])

#########################################
# Normalisation supervisée
# ------------------------
#
# Une erreur classique consiste à normaliser
# avant de séparer les données en apprentissage/test.
# Cela veut dire que des données de tests sont utilisées
# pour estimer des coefficients du modèle global
# qui inclue les prétraitements.

from sklearn.preprocessing import Normalizer
norm = Normalizer()
X_norm = norm.fit_transform(X)


#########################################
# Ce découpage pose un problème de méthodologie car la moyenne
# et la variance utilisée pour normaliser ne peuvent être estimées
# mais seulement sur la base d'apprentissage.s
# On découpage la base d'abord.
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y)

#########################################
# On normalise ensuite.
from sklearn.preprocessing import Normalizer
norm = Normalizer()
X_train_norm = norm.fit_transform(X_train)
X_test_norm = norm.transform(X_test)

#########################################
# De cette façon, la même normalisation
# est appliquée sur la base d'apprentissage et de test.
