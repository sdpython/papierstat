# -*- coding: utf-8 -*-
"""
Corrélations
============

Dessine les corrélations pour un jeu de données.
"""

###############
# A remplacer.

import os
import sys
this = os.path.abspath(os.path.dirname(__file__))
if "papierstat" in this:
    this = this.split("papierstat")[0].rstrip("\\/")
for module in ["papierstat"]:
    try:
        exec("import %s" % module)
    except ImportError:
        p = os.path.join(this, module, "src")
        sys.path.append(p)
        exec("import %s" % module)


#########################
# Récupération des données

from papierstat.datasets import load_wines_dataset
df = load_wines_dataset()
print(df.head(n=2).T)

####################
# Les corrélations avec :epkg:`seaborn`.

from seaborn import clustermap

clustermap(df.corr(), center=0, cmap="vlag",
           linewidths=.75, figsize=(13, 13))

import matplotlib.pyplot as plt
plt.show()
