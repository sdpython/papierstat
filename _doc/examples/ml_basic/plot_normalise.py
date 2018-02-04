# -*- coding: utf-8 -*-
"""
Normalisation
=============

.. contents::
    :local:

"""

###############
# A remplacer.
try:
    import papierstat
except ImportError:
    import sys
    sys.path.append("../../../src")
    import papierstat

###################
# Un jeu de données

from papierstat.datasets import load_wines_dataset
df = load_wines_dataset()
X = df.drop(['quality', 'color'], axis=1)
y = df['quality']


###################
# Normalisation naïve
# -------------------
from sklearn.preprocessing import normalize
X_norm = normalize(X)

###################
# Normalisation supervisée
# ------------------------
#######################
# Ce découpage pose un problème de méthodologie car la moyenne
# et la variance utilisée pour normaliser ne peuvent être estimées
# mais seulement sur la base d'apprentissage.s
# On découpage la base d'abord.
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y)

##############################
# On normalise ensuite.
from sklearn.preprocessing import Normalizer
norm = Normalizer()
X_train_norm = norm.fit_transform(X_train)
X_test_norm = norm.transform(X_test)

######################
# De cette façon, la même normlisation
# est appliquée sur la base d'apprentissage et de test.
