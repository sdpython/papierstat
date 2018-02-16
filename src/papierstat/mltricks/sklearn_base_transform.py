# -*- coding: utf-8 -*-
"""
@file
@brief Implémente un *transform* qui suit la même API que tout :epkg:`scikit-learn` transform.
"""
from .sklearn_base import SkBase


class SkBaseTransform(SkBase):

    """
    Base d'un *learner* which follows the same API que :epkg:`scikit-learn`.
    """

    def __init__(self, **kwargs):
        """
        Stocke les paramètres dans une classe
        @see cl SkLearnParameters, elle garde une copie des
        paramètres pour implémenter facilement *get_params*
        et ainsi cloner un modèle.
        """
        SkBase.__init__(self, **kwargs)

    ###################
    # API scikit-learn
    ###################

    def fit(self, X, y=None, sample_weight=None):
        """
        Apprends un modèle.

        @param      X               features
        @param      y               cibles
        @param      sample_weight   poids
        @return                     self, lui-même
        """
        raise NotImplementedError()

    def transform(self, X):
        """
        Prédit, souvent cela se résume à appeler la mathode *decision_function*.

        @param      X   features
        @return         prédictions
        """
        raise NotImplementedError()

    def fit_transform(self, X, y=None, sample_weight=None):
        """
        Apprends un modèle et transforme les données.

        @param      X               features
        @param      y               cibles
        @param      sample_weight   poids
        @return                     self, lui-même
        """
        self.fit(X, y=y, sample_weight=sample_weight)
        return self.transform(X)
