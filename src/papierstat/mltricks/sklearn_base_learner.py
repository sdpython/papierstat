# -*- coding: utf-8 -*-
"""
@file
@brief Implémente un *learner* qui suit la même API que tout :epkg:`scikit-learn` learner.
"""
from .sklearn_base import SkBase


class SkBaseLearner(SkBase):

    """
    Base d'un *learner* qui suit la même API que :epkg:`scikit-learn`.
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

    def predict(self, X):
        """
        Prédit, souvent cela se résume à appeler la mathode *decision_function*.

        @param      X   features
        @return         prédictions
        """
        raise NotImplementedError()

    def decision_function(self, X):
        """
        Output of the model in case of a regressor, matrix with a score for each class and each sample
        for a classifier

        @param      X   Samples, {array-like, sparse matrix}, shape = (n_samples, n_features)
        @return         array, shape = (n_samples,.), Returns predicted values.
        """
        raise NotImplementedError()

    def score(self, X, y=None, sample_weight=None):
        """
        Returns the mean accuracy on the given test data and labels.

        @param      X               Training data, numpy array or sparse matrix of shape [n_samples,n_features]
        @param      y               Target values, numpy array of shape [n_samples, n_targets] (optional)
        @param      sample_weight   Weight values, numpy array of shape [n_samples, n_targets] (optional)
        @return                     score : float, Mean accuracy of self.predict(X) wrt. y.
        """
        raise NotImplementedError()
