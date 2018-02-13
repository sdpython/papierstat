# -*- coding: utf-8 -*-
"""
@file
@brief Implémente un *transform* qui suit la même API que tout :epkg:`scikit-learn` transform.
"""
import textwrap
import numpy
from .sklearn_base_transform import SkBaseTransform
from .sklearn_base_transform_learner import SkBaseTransformLearner


class SkBaseTransformStacking(SkBaseTransform):
    """
    Un *transform* qui cache plusieurs *learners*, arrangés
    selon la méthode du `stacking <http://blog.kaggle.com/2016/12/27/a-kagglers-guide-to-model-stacking-in-practice/>`_.

    .. exref::
        :title: Stacking de plusieurs learners dans un pipeline scikit-learn.
        :tag: sklearn
        :lid: ex-pipe2learner2

        Ce *transform* assemble les résultats de plusieurs learners.
        Ces features servent d'entrée à un modèle de stacking.

        .. runpython::
            :showcode:

            from sklearn.model_selection import train_test_split
            from sklearn.datasets import load_iris
            from sklearn.linear_model import LogisticRegression
            from sklearn.tree import DecisionTreeClassifier
            from sklearn.metrics import accuracy_score
            from sklearn.pipeline import make_pipeline
            from papierstat.mltricks import SkBaseTransformStacking

            data = load_iris()
            X, y = data.data, data.target
            X_train, X_test, y_train, y_test = train_test_split(X, y)

            trans = SkBaseTransformStacking([LogisticRegression(),
                                             DecisionTreeClassifier()])
            trans.fit(X_train, y_train)
            pred = trans.transform(X_test)
            print(pred[3:])
    """

    def __init__(self, models, method=None, **kwargs):
        """
        @param  models  liste de learners
        @param  method  méthode ou list de méthodes à appeler pour
                        transformer les features (voir-ci-dessous)
        @param  kwargs  paramètres

        Options pour le paramètres *method* :

        * ``'predict'``
        * ``'predict_proba'``
        * ``'decision_function'``
        * une fonction

        Si *method is None*, la fonction essaye dans l'ordre
        ``predict_proba`` puis ``predict``.
        """
        super().__init__(**kwargs)
        if not isinstance(models, list):
            raise TypeError(
                "models must be a list not {0}".format(type(models)))
        if isinstance(method, list):
            if len(method) != len(models):
                raise ValueError("models and methods must have the same length: {0} != {1}".format(
                    len(models), len(method)))
        else:
            method = [method for m in models]
        self.models = [SkBaseTransformLearner(
            m, me) for m, me in zip(models, method)]

    def fit(self, X, y=None, sample_weight=None, **kwargs):
        """
        Apprends un modèle.

        @param      X               features
        @param      y               cibles
        @param      sample_weight   poids
        @param      kwargs          paramètres additionnels
        @return                     self, lui-même
        """
        for m in self.models:
            m.fit(X, y=y, sample_weight=sample_weight, **kwargs)
        return self

    def transform(self, X):
        """
        Prédit, souvent cela se résume à appeler la mathode *decision_function*.

        @param      X   features
        @return         prédictions
        """
        Xs = [m.transform(X) for m in self.models]
        return numpy.hstack(Xs)

    ##############
    # cloning API
    ##############

    def get_params(self, deep=True):
        """
        returns the parameters mandatory to clone the class

        @param      deep        unused here
        @return                 dict
        """
        res = self.P.to_dict()
        if deep:
            for i, m in enumerate(self.models):
                par = m.get_params(deep)
                for k, v in par.items():
                    res["estimator_{0}__".format(i) + k] = v
        return res

    def set_params(self, **params):
        """
        Set parameters.

        @param      params      parameters
        """
        for k, v in params.items():
            if not k.startswith('estimator_'):
                raise ValueError(
                    "Parameter '{0}' must start with 'estimator_'.".format(k))
        d = len('estimator_')
        pars = [{} for m in self.models]
        for k, v in params.items():
            si = k[d:].split('__', 1)
            i = int(si[0])
            pars[i][k[d + 1 + len(si):]] = v
        for p, m in zip(pars, self.models):
            if p:
                m.set_params(**p)

    #################
    # common methods
    #################

    def __repr__(self):
        """
        usual
        """
        rps = repr(self.P)
        res = "{0}([{1}], [{2}], {3})".format(
            self.__class__.__name__,
            ", ".join(repr(m.model) for m in self.models),
            ", ".join(repr(m.method) for m in self.models), rps)
        return "\n".join(textwrap.wrap(res, subsequent_indent="    "))
