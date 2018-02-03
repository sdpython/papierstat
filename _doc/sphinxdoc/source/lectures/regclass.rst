
.. _l-regclass:

============================
Classification et régression
============================

Le site :epkg:`UCI` propose de nombreux jeux de
de données utilisés dans un but pédagogique.
Parmi ceux-ci, on y trouve un jeu de données
sur le vin, `Wine Data Set <https://archive.ics.uci.edu/ml/datasets/wine+quality>`_.
Pour ma part, j'ai goûté le vin assez tard, ne sachant véritablement
l'apprécier qu'à la trentaine avérée. Je suis encore incapable de
déchiffrer le vocabulaire qui sort de la bouche des experts
pour me contenter d'un *"j'aime"* ou *"j'aime pas"* loin
du caractère tanique ou parfumé du breuvage. Culture française
oblige, ce jeu de données pourrait convertir les mesures
issues d'une pipette, les composants chimiques du vin,
en une note gustative. Ce jeu est intéressant car il montre
que ce n'est pas si simple. J'aimerais pouvoir estimer la qualité
d'un vin en fonction de sa composition chimique. Deux usages
à cela, le premier pour choisir un vin sans avoir à le goûter,
le second s'il me prend l'envie d'être viticulteur afin
de pouvoir améliorer la qualité d'un vin en jouant sur ses
composants.

.. contents::
    :local:

* `Problèmes classiques de machine learning illustrés <http://www.xavierdupre.fr/app/ensae_teaching_cs/helpsphinx3/notebooks/ml_c_machine_learning_problems.html>`_
* `Machine Learning par Gaël Varoquaux <http://www.xavierdupre.fr/app/ensae_teaching_cs/helpsphinx3/all_notebooks.html#a-sklearn-ensae-course>`_

Finalité du machine learning
++++++++++++++++++++++++++++

On ne part pas de rien pour construire cette fonction, on dispose
de plusieurs milliers de notes données par des experts à des milliers
de vins dont on connaît les mêmes 12 informations sur leur composition,
ci-dessous, pour deux vins.

.. runpython::
    :rst:

    from pyquickhelper.pandashelper import df2rst
    from papierstat.datasets import load_wines_dataset
    df = load_wines_dataset()
    print(df2rst(df.head(n=2).T.reset_index(drop=False)))

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
on obtiendrait le graphe suivant en positionnant chaque vin noté dans
la base en fonction de sa composante et de sa note.

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
    from papierstat.datasets import load_wines_dataset
    df = load_wines_dataset()
    df = df[['fixed_acidity', 'volatile_acidity', 'citric_acid', 'quality']].copy()
    df['...'] = '...'
    print(df2rst(df.head()))

.. plot::

    from papierstat.datasets import load_wines_dataset
    df = load_wines_dataset()

    import matplotlib.pyplot as plt
    plt.close('all')
    plt.style.use('ggplot')
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10,4))
    df.quality.hist(bins=18, ax=ax)
    plt.title('Distribution des notes des vins')
    plt.show()

Il y a plus de 6000 vins répertoriés.
Les très mauvais ou très bons vins sont peu nombreux,
c'est-à-dire que les notes sont distribuées de façon non uniforme.
Cela aura son importance plus tard. Toutefois, si la prédiction
dépend des observations passées, il est probable que le modèle soit
plus à l'aise là où il a le plus d'information. Les vins extrêmes,
peu représentés, seront sans doute moins bien appréhendés par
le modèle de prédiction.

.. toctree::
    :maxdepth: 1

    notebooks/wines_knn_acp

.. index:: plus proches voisins

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
De façon un peu plus mathématique, on considère les données d'apprentissage
:math:`(X_i, y_i)_{i=1}^n`, le modèle construit une prédiction pour un :math:`x`
donné à partir de :math:`k` plus proches voisins. Ceux-ci vérifie :

.. math::

    \begin{array}{ll} V(k, X) = \acc{ i_{\sigma(1)}, ..., i_{\sigma(k)}} \\
    \text{avec} \; d(X, X_{\sigma(1)}) \leqslant ... \leqslant d(X, X_{\sigma(k)}) \leqslant d(X, X_j) \;
    \forall j \notin \acc{\sigma(1), ..., \sigma(k)} \end{array}

La prédiction est une moyenne des valeurs connues associées aux voisins trouvés :

.. math::

    f(X, k) = \frac{\sum_{i=1}^k y_{\sigma(i)}}{k}

Il s'agit maintenant d'appliquer cet algorithme afin de
prédire la note d'un vin pour trois vins représentés par
les trois points d'interrogations qui suivent.

.. image:: images/predict.png
    :width: 200

Cette représentation simplifiée montre deux vins
plutôt simples à classer et un dernier - cercle jaune -
dont les voisins sont en désaccord quant à la décision
à prendre. Le vrai visage du jeu de données est plus
difficile à lire. Il est obtenu grâce à une
`analyse en composante principale (ACP) <https://fr.wikipedia.org/wiki/Analyse_en_composantes_principales>`_
qui projette un ensemble de points dans un espace de dimension réduite
en maximisant la variance de l'ensemble projeté.

.. image:: images/acp.png
    :width: 300

Peut-être que la prédiction sera facile mais ce n'est
pas cette représentation qui permet de nous en assurer.

.. toctree::
    :maxdepth: 1

    ../notebooks/wines_knn
    ../notebooks/wines_knn_eval

.. index:: ball tree

Les plus proches voisins est un des modèles les plus simples
avec le modèle linéaire, il est néanmoins très coûteux à calculer
puisqu'il faut a priori s'enquérir de toutes les distances entre
un nouveau point et ceux déjà connus. Des algorithmes permettent
d'accélérer la recherche de voisins comme les
`ball tree <https://en.wikipedia.org/wiki/Ball_tree>`_.
Ils sont de moins en moins
efficaces au fur et à mesure que la dimension de l'espace
des features augmente :
`Nearest Neighbours and Sparse Features <http://www.xavierdupre.fr/app/ensae_projects/helpsphinx/notebooks/nearest_neighbours_sparse_features.html>`_.

.. index:: bases d'apprentissage et de test, train_test_split

Train / test
++++++++++++

Il n'est pas facile d'avoir une idée la pertinence
d'un modèle de prédiction. Le plus simple est de
comparer les prédictions obtenus avec la valeur de l'expert.
Comme le modèle des plus proches voisins retourne
toujours la bonne prédiction s'il a déjà vu un vin,
il faut nécessairement pouvoir lui en proposer de nouveau.

La base de données représente l'ensemble des données
à disposition. Il est impossible d'en amener de nouvelles
pour le moment. Il faudra s'en contenter.
On découpe alors les données en deux ensembles,
un pour apprendre, un pour tester. On les appelle
les bases d'apprentissage et de test. On compare
les prédictions aux valeurs attendues sur la base
de test.

.. toctree::
    :maxdepth: 1

    ../notebooks/wines_knn_split
    ../notebooks/wines_knn_split_strat

.. index:: validation croisée, cross-validation

Validation croisée
++++++++++++++++++

Il est acquis qu'un modèle doit être évalué sur une base de test différente
de celle utilisée pour l'apprentissage. Mais la performance est peut-être
juste l'effet d'une aubaine et d'un découpage particulièrement avantageux.
Pour être sûr que le modèle est robuste, on recommence plusieurs fois. On appelle
cela la *validation croisée* ou
`cross validation <https://en.wikipedia.org/wiki/Cross-validation_(statistics)>`_
en anglais. La base de données en découpée en :math:`n` segments,
5 le plus souvent, 4 segments servent à apprendre, le dernier
à tester. On permute 5 fois et cela donne cinq scores.

.. image:: images/cross.png
    :width: 200

.. toctree::
    :maxdepth: 1

    ../notebooks/wines_knn_cross_val

.. index:: hyper-paramètre

Hyper-paramètres
++++++++++++++++

Un modèle de :epkg:`machine learning` est appris avec un
algorithme d'optimisation. Celui dépend de plusieurs paramètres,
le nombre de voisins dans le cas des plus proches voisins,
le pas de gradient pour un
`algorithme de descente de gradient <https://fr.wikipedia.org/wiki/Algorithme_du_gradient>`_.
Il est illusoire de penser que les mêmes paramètres donnent les meilleurs
résultats quelque soit le jeu de données considéré. Mais alors,
quels paramètres donnent les meilleurs résultats ?
La plus simple stratégie est d'essayer plusieurs valeurs et de
choisir la meilleure.

.. toctree::
    :maxdepth: 1

    ../notebooks/wines_knn_hyper

.. index:: régression

Régression
++++++++++

Le bruit blanc est une variable aléatoire couramment utilisé
pour désigner le hasard ou la part qui ne peut être modélisée
dans une régression ou tout autre problème d'apprentissage.
On suppose parfois que ce bruit suive une loi normale.

.. mathdef::
    :title: bruit blanc
    :tag: Définition
    :lid: def-bruit-blanc

    Une suite de variables aléatoires réelles
    :math:`\pa{\epsilon_i}_{1 \infegal i \infegal N}`
    est un bruit blanc :

    * :math:`\exists \sigma > 0`, :math:`\forall i \in \intervalle{1}{N}, \; \epsilon_i \sim \loinormale{0}{\sigma}`
    * :math:`\forall \pa{i,j} \in \intervalle{1}{N}^2, \; i \neq j \Longrightarrow \epsilon_i \independant \epsilon_j`

La prédiction de la note des vins est un problème de
`régression <http://www.xavierdupre.fr/app/mlstatpy/helpsphinx/c_ml/rn/rn_2_reg.html>`_
et cela consiste à résoudre le problème suivant :

.. mathdef::
    :title: Régression
    :tag: Problème
    :lid: problem-regression

    Soient deux variables aléatoires :math:`X` et :math:`Y`,
    l'objectif est d'approximer la fonction
    :math:`\esp\pa{Y | X} = f\pa{X}`.
    Les données du problème sont
    un échantillon de points :math:`\acc{ \pa{ X_{i},Y_{i} } | 1 \infegal i \infegal N }`
    et un modèle paramétré avec :math:\theta` :

    .. math::

            \forall i \in \intervalle{1}{N}, \; Y_{i} = f \pa{\theta,X_{i}} + \epsilon_{i}

    avec :math:`n \in \N`,
    :math:`\pa{\epsilon_{i}}_{1 \infegal i \infegal N}` :ref:`bruit blanc <def-bruit-blanc>`,
    :math:`f` est une fonction de paramètre :math:`\theta`.
		

La fonction :math:`f` peut être une fonction linéaire,
un polynôme, un réseau de neurones...
Lorsque le bruit blanc est normal, la théorie de l'estimateur
de vraisemblance (voir [Saporta1990]_) permet d'affirmer
que le meilleur paramètre :math:`\hat{\theta}`
minimisant l'erreur de prédiction est :

.. math::

    \hat{\theta} = \underset {\theta \in \R^p}{\arg \min} \; \esp \pa {\theta}
			     = \underset {\theta \in \R^p}{\arg \min}
                   \cro{ \sum_{i=1}^{N} \cro{Y_{i}-f \pa{\theta,X_{i}}}^{2}}

Le lien entre les variables :math:`X` et :math:`Y` dépend des hypothèses faites
sur :math:`f`. Généralement, cette fonction n'est supposée non linéaire
que lorsqu'une `régression linéaire <https://fr.wikipedia.org/wiki/R%C3%A9gression_lin%C3%A9aire>`_
donne de mauvais résultats.

-----------------------

apprentissage

évaluation

Classification
++++++++++++++

apprentissage

évaluation

Score de classification et courbe ROC
+++++++++++++++++++++++++++++++++++++

Modèles ou features
+++++++++++++++++++

`Features ou modèle <http://www.xavierdupre.fr/app/ensae_teaching_cs/helpsphinx3/notebooks/ml_features_model.html>`_
