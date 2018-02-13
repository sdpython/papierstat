# -*- coding: utf-8 -*-
"""
@file
@brief Implémente un *transform* qui suit la même API que tout :epkg:`scikit-learn` transform.
"""
import textwrap
from .sklearn_parameters import SkLearnParameters


class SkBaseTransform:

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
        self.P = SkLearnParameters(**kwargs)

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

    def get_params(self, deep=True):
        """
        returns the parameters mandatory to clone the class

        @param      deep        unused here
        @return                 dict
        """
        return self.P.to_dict()

    def __repr__(self):
        """
        usual
        """
        res = "{0}({1})".format(self.__class__.__name__, str(self.P))
        return "\n".join(textwrap.wrap(res), subsequent_indent="    ")
