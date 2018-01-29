
Classification et régression
============================

Le site :epkg:`UCI` propose de nombreux jeux de
de données utilisés dans un but pédagogique.
Parmi ceux-ci, on y trouve un jeux de données
sur le vin, `Wine Data Set <https://archive.ics.uci.edu/ml/datasets/wine>`_.
Pour ma part, j'ai goûté le vin assez tard, ne sachant véritablement
l'apprécier qu'à la trentaine avérée. Je suis encore incapable de
déchiffrer le vocabulaire qui sort de la bouche des experts
pour me contenter d'un *"j'aime"* ou *"j'aime pas"* loin
du caractère tanique du breuvage. Culture française
oblige, ce jeu de données pourrait convertir les mesures
issues d'une pipette, les composants chimiques du vin,
en une note gustative. Ce jeu est intéressant car il montre
que ce n'est pas si simple. J'aimerais pouvoir estimer la qualité
d'un vin en fonction de sa composition chimique. Deux usages
à cela, le premier pour choisir un vin sans avoir à le goûter,
le second s'il me prend l'envie d'être viticulteur,
de pouvoir améliorer la qualité d'un vin en jouant sur ses
composants.

.. contents::
    :local:

Finalité du machine learning
++++++++++++++++++++++++++++

On ne part pas de rien pour construire cette fonction, on dispose
de plusieurs milliers de notes données par des experts à des milliers
de vins dont on connaît les mêmes 12 informations sur leur composition.

.. runpython::
    :rst:

    from pyquickhelper.pandashelper import df2rst
    from papierstat.datasets import load_wines_datasets
    df = load_wines_datasets()
    print(df2rst(df.head(n=2).T))

On part du principe que si deux vins différents ont la même
composition, leurs qualités gustatives seront identiques.
6000 vins c'est à la fois beaucoup et pas beaucoup.
Si un vin inconnu a une composition identique à l'un des 6000 vins
répertoriés, on peut supposer qu'il obtiendra la même note.
Mais si sa composition est tout aussi nouvelle, que faire ?

Un des objectifs du :epkg:`machine learning` est de proposer
une façon de construire une note pour une composition nouvelle.
On appelle cela faire une **prédiction**. On souhaite en quelque sorte
étendre le savoir accumulé sur 6000 vins à de nouvelles compositions
de vins. Si les vins n'avaient qu'un seul composant chimique,
on obtiendrait ce genre de graphes en positionnant sur ce graphe
chaque vin noté dans la base.

.. image:: images/ques.png
    :width: 300

Le trait vert correspond à la concentration de ce composé
pour un nouveau vin et elle est différente de toutes celles connues.
On se doute que la qualité de ce nouveau vin sera dans le cercle bleu
mais où ? C'est ce que nous allons voir.

Les données
+++++++++++

Le jeu de données peut être téléchargé depuis le site
`Wine Quality Data Set <https://archive.ics.uci.edu/ml/datasets/wine+quality>`_.
Il peut être également obtenu avec le code suivant :

.. runpython::
    :showcode:
    :rst:

    from pyquickhelper.pandashelper import df2rst
    from papierstat.datasets import load_wines_datasets
    df = load_wines_datasets()
    print(df2rst(df.head()))

Il y a plus de 6000 répertoriés
Et les notes sont distribuées de façon non uniformes,
cela aura son importance plus tard.

.. plot::

    from papierstat.datasets import load_wines_datasets
    df = load_wines_datasets()

    import matplotlib.pyplot as plt
    plt.close('all')
    plt.style.use('ggplot')
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10,4))
    df.quality.hist(bins=18, ax=ax)
    plt.show()

Les plus proches voisins
++++++++++++++++++++++++

Le modèle de prédiction le plus intuitif consiste à chercher pour
chaque nouveau vin le vin qui lui ressemble le plus parmi tous ceux connus.
On appelle cette méthode la méthode des
`plus proches voisins <https://fr.wikipedia.org/wiki/Recherche_des_plus_proches_voisins>`_.
Le module :epkg:`scikit-learn` implémente cet algorithme
`Nearest Neighbors <http://scikit-learn.org/stable/modules/neighbors.html>`_ et
on pourra s'inspirer de l'exemple
`Nearest Neighbors regression <http://scikit-learn.org/stable/auto_examples/neighbors/plot_regression.html#sphx-glr-auto-examples-neighbors-plot-regression-py>`_.

.. toctree::
    :max_depth: 1

    notebooks/wines_knn
    notebooks/wines_knn_eval

Train / test
++++++++++++

Un modèle de régression
+++++++++++++++++++++++

apprentissage

évaluation

Même problème sous l'angle de la classification
+++++++++++++++++++++++++++++++++++++++++++++++

apprentissage

évaluation

Les vins bons sont rares
++++++++++++++++++++++++

smote

Modèles non linéaires
+++++++++++++++++++++

Modèles continus et méthodes ensemblistes
+++++++++++++++++++++++++++++++++++++++++
