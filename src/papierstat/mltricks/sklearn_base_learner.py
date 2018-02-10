# -*- coding: utf-8 -*-
"""
@file
@brief Implémente un *learner* qui suit la même API que tout :epkg:`scikit-learn` learner.
"""

from .sklearn_parameters import SkLearnParameters


class SkBaseLearner:

    """
    Base d'un *learner* which follows the same API que :epkg:`scikit-learn`.
    """

    def __init__(self, **kwargs):
        """
        Stocke les paramètres.
        """

        #: *P* est une instance de :class:`SkLearnParameters <ensae_teaching_cs.ml.sklearn_parameters.SkLearnParameters>`,
        #: elle garde une copie des paramètres pour implémenter facilement *get_params*
        #: et ainsi cloner un modèle
        self.P = SkLearnParameters(**kwargs)

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

    ##############
    # cloning API
    ##############

    def get_params(self, deep=True):
        """
        returns the parameters mandatory to clone the class

        @param      deep        unused here
        @return                 dict
        """
        return self.P.to_dict()

    #################
    # common methods
    #################

    def __str__(self):
        """
        usual
        """
        return "{0}({1})".format(self.__class__.__name__, str(self.P))
