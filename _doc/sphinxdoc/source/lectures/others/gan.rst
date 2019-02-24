
.. _l-gan:

Generative Adversarial Nets (GAN)
=================================

Cette idée est décrite dans l'article
`Generative Adversarial Nets <https://arxiv.org/pdf/1406.2661.pdf>`_
et depuis abbréviée simple en *GAN*. C'est une idée
plutôt élégante et qui mérite qu'on s'y arrête un peu plus.
Elle repose sur une couple de modèles, l'un qui simule
des données, l'autre, un classifieur, qui détermine si le premier
modèle simule des données proches d'un ensemble de données initial.
Les deux modèles convergent vers l'un modèle capable de générer
des données proches de vraies données, l'autre capable de différencier
entre des fausses et des vraies données.

.. contents::
    :local:

Algorithme
++++++++++

En quelques mots, cela commence par un jeu de données
:math:`X_1, ..., X_m`. On commence par un générateur
:math:`G(\Theta, z)` où *z* est une variable aléatoire
qui sert à générer des observations
:math:`Y_1, ..., Y_m` pour construire un jeu de données
:math:`(X_1, 1), ..., (X_m, 1), (Y_1, 0), ..., (Y_m, 0)`,
un classifieur est ensuite appris pour distinguer les vraies
observations des fausses. On l'appelle le *discriminateur*
:math:`D(\Omega, X)`. A partir de là, on peut calculer un
gradient :math:`\partial D / \partial X` qui sert à améliorer
la qualité du générateur. Et on recommence...

#. Générer aléatoirement des observations *z*.
#. Utiliser le générateur pour générer des observations
   :math:`Y_1, ..., Y_m`.
#. Apprendre le classifieur sur le jeu
   :math:`(X_1, 1), ..., (X_m, 1), (Y_1, 0), ..., (Y_m, 0)`.
#. Mettre à jour le générateur.
#. Recommencer jusqu'à convergence.

En termes plus mathématiques...

.. mathdef::
    :tag: théorème
    :title: Minibatch stochastic gradient descent training of generative adversarial nets

    #. Sample minibatch of *m* noise samples *z(1), ..., z(m)*
       from noise prior *G(z)*.
    #. Sample minibatch of *m* examples *x(1), ..., x(m)*
       from data generating distribution *data(x)*.
    #. Update the discriminator by ascending its stochastic gradient:

       .. math::

            \nabla_\Theta

    #. Sample minibatch of *m* noise samples *z(1), ..., z(m)*
       from noise prior *G(z)*.
    #. Update the generator by descending its stochastic gradient:

        .. math::

            \nabla_\Omega

    The gradient-based updates can use any standard gradient-based learning rule.
    We used momentum in our experiments.
