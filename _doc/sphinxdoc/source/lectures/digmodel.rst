
Comprendre un modèle
====================

Le seul modèle qu'on comprend vraiment bien est le
modèle linéaire. C'est le seul qui soit facilement
interprétable et dont on connaisse les propriétés.
En dehors ce modèle, l'expérimentation est souvent
la seule réponse à la question : que se passe-t-il
si les données utilisées pour la prédiction sont
différentes de celles utilisées pour l'apprentissage ?
Dans la grande majorité des cas, on suppose
que les données utilisées pour la prédiction suivent
la même loi que les données d'apprentissage et c'est
ce qui fait que la prédiction est *fiable*.
Les données ne sont jamais rigoureusement semblables
à celles qui les ont précédés et il est courant
d'observer une forme de dérive des performances de
prédictions au cours du temps. C'est un phénomène
facile à observer lorsque la dimension du problème
est faible, plus difficile à détecter lorsque le nombre
de variable est grand. Reste l'intuition que cela peut
arriver.

.. toctree::
    :maxdepth: 1

    ../notebooks/artificiel_shape
    ../notebooks/logreg_kmeans
