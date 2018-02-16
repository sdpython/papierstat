
.. blogpost::
    :title: Automatiser des expériences de machine learning
    :keywords: scikit-learn, automatisation
    :date: 2018-02-16
    :categories: scikit-learn

    Prenons un exemple car le titre est assez flou.
    On souhaite apprendre deux modèles différents
    sur deux parties disjointes d'un jeu de données :
    la prédiction de la qualité d'un vin selon qu'il est
    blanc ou rouge. Selon que le vin est blanc ou rouge,
    on n'appliquera pas le même modèle. L'ensemble
    tient en quelques lignes dans un notebook mais comme
    cette idée revient souvent, on peut être tenté de l'implémenter
    une bonne fois pour toutes sous la forme d'un modèle
    qui s'intègre facilement avec :epkg:`scikit-learn`.
    C'est ce que propose la classe
    :class:`SkBaseLearnerCategory <papierstat.mltricks.sklearn_base_learner_category.SkBaseLearnerCategory>`.
    Ce point est abordé de façon plus détaillée :
    :ref:`l-sklearn-programmation`.
