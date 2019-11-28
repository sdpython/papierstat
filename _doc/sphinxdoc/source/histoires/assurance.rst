
Assurance auto
==============

.. contents::
    :local:

J'avoue que je ne savais pas trop où allait partir cette
séance de cours quand je l'ai commencée avec seulement
l'idée qu'on n'a pas toujours besoin des données pour
prédire ce qu'elle pourrait nous raconter si nous les avions.
Et pourquoi ne pas supposer que nous les avons...
J'ai donc demandé aux étudiants quelques problèmes
de prédiction qui pourrait intéresser une compagnie
d'assurance. Deux réponses sont restées, la fait qu'un
client reste client et ne parte pas pour une autre assurance,
et la prédiction d'un risque. Le risque est une notion
assez floue et qui nécessite quelques éclaircissements
avant d'utiliser des outils comme le machine learning.
Les maths n'aiment pas l'imprécision et tout ce qui
n'est pas quantifiable. Je dis cela même si je ne sais
pas vraiment compter. Je sais que je sais comment compter,
je sais que je ne sais pas faire deux fois le même calcul
et retrouve le même résultat. Je ne vais pas compter donc.
Nous sommes partis pour l'assurance auto même si je n'ai
pas le permis et que mon rêve est que les chauffeurs
disparaissent.

Assurance auto
++++++++++++++

L'assurance est un moyen de mutualiser les risques.
C'est-à-dire les conséquences financières d'un accident
puisque nous vivons dans une économie où tout a quasiment
une correspondance en argent. Le risque est donc l'ensemble
des dépenses financières. De quelles données faut-il disposer
pour estimer ces dépenses ?

Il nous faut une liste de sinistres avec les dépenses
financières associées, la date de chaque sinistre. Si on
veut moduler le risque en fonction d'autres facteurs,
comme l'âge, le genre, la marque de la voiture, le modèle,
la ville.

Mais comment mesurer un risque si on ne connaît que les accidents ?
Cela revient à dire que toutes les personnes de la base de
de données ont eu un accident ce qui n'est pas le but souhaité.
On peut ajouter à la liste des autres clients qui n'ont pas
eu d'accidents. Mais il semble que quelque chose manque.
La probabilité d'avoir un accident sur une vie est plus
importante que celle d'avoir un accident dans l'année qui suit.
Cela veut dire aussi qu'une personne n'est plus une seule
observation mais plusieurs, une pour chaque année. Cela permet
aussi de prendre en compte le fait qu'une personne change souvant
plusieurs fois de voiture tout au long de sa vie.

Données
+++++++

Ce problème est toujours théorique mais pour la suite,
on suppose que les données sont organisées dans une table
avec les colonnes suivantes :

* année
* identifiant personne
* âge
* genre
* modèle
* âge voiture
* kilométrage
* adresse sous la forme longitude lattitude,
  ou celle du centre du quartier pour anonymiser
  les données même si couplées aux autres variables,
  il existe sans doute un nombre réduit de personnes
  avec le même âge et la même voiture, pour la suite,
  nous considérerons que le modèle utilise les coordonnées
  de l'adresse
* montant du sinistre durant l'année suivante = Y

La dernière colonne est celle que nous souhaitons
prédire, elle correspond au risque et elle est nulle
la plupart du temps. On pourrait également se demander
pourquoi un an, pourquoi pas une semaine ? Mais plus
l'horizon est court, plus cette probabilité est pour le
moins difficile à évaluer et de plus en plus faible.
Il faut se fixer un horizon raisonnable.

Premier réflexe : apprentissage et test
+++++++++++++++++++++++++++++++++++++++

Le machine learning sert à prédire, il a tendance
à faire du surapprentissage dès qu'il en a la possibilité.
C'est pourquoi on divise la base dont on dispose en
base d'apprentissage et base de test. La base en cours
n'est pas une série temporelle mais il a une
composante temporelle. Cela veut dire qu'il faudra
faire attention à ne pas utiliser les informations
du futur pour prédire. Une **division selon une année** paraît
le plus simple pour découper la base.

Il existe une autre possibilité, celle de répartir chaque
client selon une base ou une autre. Cela permet d'éviter
que les données le passé d'un client soient en quelque
sorte mémorisé par le modèle pour prédire son futur dans la
base de test. Une division par client est l'assurance que le
modèle pourra s'adapter à des personnes qu'il n'a jamais vues.

Une division par modèle ou par âge rendrait le modèle incapable
de prédire pour toute nouvelle personne. Donc,
dans un premier temps une **division par personne** semble
le mieux adapté.

Il faudra utiliser les deux divisions à la fin pour s'assurer
que le modèle est robuste mais pour le moment,
cette division non temorelle est la plus simple.

Ajout de variables agrégées
+++++++++++++++++++++++++++

Parmi les variables qui permettent d'améliorer
la performance du modèle, il y a des statistiques agrégées
comme la probabilité d'avoir un accident avec tel ou tel
modèle de voiture, ou après un certain âge. Il faut à chaque fois
faire attention au temps.

La probabilité d'avoir un accident avec tel ou tel modèle
ne peut être calculée que les données passées au moment
où elle est considérée, ce nombre évoluera chaque année
pour une même personne.

Il est difficile d'estimer la probabilité d'avoir un accident
après un certain âge lorsque la variable à prédire fait elle
partie de l'agrégation qui est construite.
Il faut donc exclure la personne considéré avant de calculer ce
taux qui sera donc différent pour chacun. La pertinence du
modèle est plus simple à vérifier alors avec une division
apprentissage / test selon les personnes. Et pour la base
de test, il faudra s'assurer que les variables agrégées
soient calculées uniquement avec la base d'apprentissage.

Données géographiques
+++++++++++++++++++++

On s'aperçoit que les données géographiques ne sont
absolument pas utilisées par le modèle même s'il
paraît intuitif que certaines régions d'un pays
sont plus propices aux accidents. D'un autre côté,
il est improbable de trouver une corrélation entre
la latitude et le risque. Pourquoi serait-il plus risqué
de conduire au Nord plutôt qu'au Sud de la France ?

Pour utiliser cette variable, il faut regrouper les
habitants en zones. Faire un clustering en quelque sorte.
Le problème avec cette approche est qu'elle aboutira
à créer des zones très denses dans les villes et d'autres moins.
On peut constraindre le clustering à ne regrouper que plusieurs
milliers de personnes ou simplement utiliser le graphe
d'une classification ascendante hiérarchique pour regrouper
10.000 personnes dans chaque zone.

Grand nombre de variables
+++++++++++++++++++++++++

Pour que la clusterisation ait un impact, il faudra
sans doute beaucoup de clusters et le numéro de cluster
d'une personne est une variable catégorielle qu'on a l'habitude
de traiter avec un :epkg:`OneHotEncoder` qui crée une variable
pour chaque cluster. Il est alors probable que le nombre de
variables dépasse le nombre d'observations.
Il faut réduire la dimension !

Une ACP paraît le plus indiquée mais cela a-t-il vraiment un sens ?
On est sûr d'une chose, le modèle sera difficilement interprétable si
sa performance dépend fortement de la région géographique.
Une autre idée consiste à faire une moyenne du risque sur chaque zone,
et plutôt que d'utiliser la zone géographique, on utilise
les autres variables agrégées sur cette zone. De cette façon,
le nombre de variables reste petit. Là encore, il faut faire
attention à ne pas mélanger passé et futur.

Modélisation un peu plus anonyme
++++++++++++++++++++++++++++++++

La prédiction est personnalisée mais elle requiert de
connaître une personne beaucoup d'informations souvent
considéré comme sensible. C'est pourquoi, on peut construire
un modèle qui estime le risque annuel d'un côté pour des groupes
d'individus et qui le multiplie par la fréquence des accidents
d'une personne en particulier :
*risque(personne) = risque(groupe) * fréquence(accident / personne)*.
Cela permet de réduire la part des informations personnelles
à un simple facteur.
