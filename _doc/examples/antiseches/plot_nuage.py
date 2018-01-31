# -*- coding: utf-8 -*-
"""
Corrélations
============

Dessine les corrélations pour un jeu de données.
"""

###############
# A remplacer.
try:
    import papierstat
except ImportError:
    import sys
    sys.path.append("../../../src")
    import papierstat

#########################
# Récupération des données

from papierstat.datasets import load_wines_dataset
df = load_wines_dataset()
print(df.head(n=2).T)

####################
# Les corrélations avec :epkg:`seaborn`.

from seaborn import clustermap

clustermap(df.corr(), center=0, cmap="vlag", linewidths=.75, figsize=(4, 4))

import matplotlib.pyplot as plt
# plt.show()
