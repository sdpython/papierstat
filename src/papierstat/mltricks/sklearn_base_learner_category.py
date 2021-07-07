# -*- coding: utf-8 -*-
"""
@file
@brief Implémente un *learner* qui suit la même API que tout :epkg:`scikit-learn` learner.
"""
import numpy
import pandas
from sklearn.base import clone
from mlinsights.sklapi import SkBaseLearner, SkLearnParameters


class SkBaseLearnerCategory(SkBaseLearner):

    """
    Base d'un *learner* qui apprend un learner pour chaque
    modalité d'une classe.

    Notebooks associés à ce *learner* :

    .. runpython::
        :rst:

        from papierstat.datasets.documentation import list_notebooks_rst_links
        links = list_notebooks_rst_links('lectures', 'wines_color_linear')
        links = ['    * %s' % s for s in links]
        print('\\n'.join(links))
    """

    def __init__(self, colnameind=None, model=None, **kwargs):
        """
        Stocke les paramètres dans une classe
        @see cl SkLearnParameters, elle garde une copie des
        paramètres pour implémenter facilement *get_params*
        et ainsi cloner un modèle.

        @param      colnameind  indice ou nom de la colonne qui
                                contient les modalités de la catégorie
        @param      model       model à appliquer sur chaque catégorie
        """
        if not isinstance(colnameind, (int, str)):
            raise TypeError(  # pragma: no cover
                "colnameind must be str or int not {0}".format(type(colnameind)))
        if model is None:
            raise ValueError("model must not be None")  # pragma: no cover
        kwargs['colnameind'] = colnameind
        SkBaseLearner.__init__(self, **kwargs)
        self.model = model
        self._estimator_type = self.model._estimator_type

    @property
    def colnameind(self):
        """
        Retourne le nom ou l'indice de la catégorie.
        """
        return self.P.colnameind

    @property
    def Models(self):
        """
        Retourne les models.
        """
        if hasattr(self, 'models'):
            return self.models
        raise RuntimeError('No trained models')  # pragma: no cover

    def _get_cat(self, X):
        """
        Retourne les catégories indiquées par *colnameind*.
        """
        if isinstance(self.colnameind, str):
            if not hasattr(X, 'columns'):
                raise TypeError(  # pragma: no cover
                    "colnameind='{0}' and X is not a DataFrame but {1}".format(
                        self.colnameind, type(X)))
            return X[self.colnameind]
        return X[:, self.colnameind]

    def _filter_cat(self, c, X, y=None, sample_weight=None):
        """
        Retoure *X*, *y*, *sample_weight* pour la categorie *c* uniquement.
        """
        indices = numpy.arange(0, X.shape[0])
        if isinstance(self.colnameind, str):
            if not hasattr(X, 'columns'):
                raise TypeError(  # pragma: no cover
                    "colnameind='{0}' and X is not a DataFrame but {1}".format(
                        self.colnameind, type(X)))
            ind = X[self.colnameind] == c
            sa = None if sample_weight is None else sample_weight[ind]
            y = None if y is None else y[ind]
            ind, x = indices[ind], X.drop(self.colnameind, axis=1)[ind]
        elif hasattr(X, 'iloc'):
            ind = X[self.colnameind] == c
            sa = None if sample_weight is None else sample_weight[ind]
            y = None if y is None else y[ind]
            ind, x = indices[ind], X.iloc[ind, -self.colnameind]
        else:
            ind = X[self.colnameind] == c
            sa = None if sample_weight is None else sample_weight[ind]
            y = None if y is None else y[ind]
            ind, x = indices[ind], X[ind, -self.colnameind]
        if y is not None and x.shape[0] != y.shape[0]:
            raise RuntimeError(  # pragma: no cover
                "Input arrays have different shapes for value='{0}': {1} != {2} "
                "(expected: {3}) type(X)={4}".format(
                    c, X.shape[0], y.shape[0], ind.shape, type(X)))
        if sa is not None and x.shape[0] != sa.shape[0]:
            raise RuntimeError(  # pragma: no cover
                "Input arrays have different shapes for value='{0}': {1} != {2} "
                "(expected: {3}) type(X)={4}".format(
                    c, X.shape[0], sa.shape[0], ind.shape, type(X)))
        return ind, x, y, sa

    ###################
    # API scikit-learn
    ###################

    def fit(self, X, y=None, sample_weight=None, **kwargs):
        """
        Apprends un modèle pour chaque modalité d'une catégorie.

        @param      X               features
        @param      y               cibles
        @param      sample_weight   poids de chaque observation
        @return                     self, lui-même

        La fonction n'est pas parallélisée mais elle le pourrait.
        """
        cats = set(self._get_cat(X))
        for c in cats:
            if not isinstance(c, str) and numpy.isnan(c):
                raise ValueError(  # pragma: no cover
                    "One of the row has a missing category.")

        res = {}
        for c in sorted(cats):
            _, xcat, ycat, scat = self._filter_cat(c, X, y, sample_weight)
            mod = clone(self.model)
            if scat is not None:
                kwargs['sample_weight'] = scat
            mod.fit(xcat, ycat, **kwargs)
            res[c] = mod
        self.models = res
        return self

    def _any_predict(self, X, fct, *args):
        """
        Prédit en appelant le modèle associé à chaque catégorie.

        @param      X   features
        @return         prédictions

        La fonction n'est pas parallélisée mais elle le pourrait.
        """
        cats = set(self._get_cat(X))
        for c in cats:
            if not isinstance(c, str) and numpy.isnan(c):
                raise NotImplementedError(  # pragma: no cover
                    "No default value is implemented in case of missing value.")

        res = []
        for c in sorted(cats):
            ind, xcat, ycat, _ = self._filter_cat(c, X, *args)
            mod = self.models[c]
            meth = getattr(mod, fct)
            if ycat is None:
                pred = meth(xcat)
            else:
                pred = meth(xcat, ycat)
            if len(pred.shape) == 1:
                pred = pred[:, numpy.newaxis]
            if len(ind.shape) == 1:
                ind = ind[:, numpy.newaxis]
            pred = numpy.hstack([pred, ind])
            res.append(pred)
        try:
            final = numpy.vstack(res)
        except ValueError:  # pragma: no cover
            # Only one dimension.
            final = numpy.hstack(res)
        df = pandas.DataFrame(final)
        df = df.sort_values(
            df.columns[-1]).reset_index(drop=True)  # pylint: disable=E1136
        df = df.iloc[:, :-1].values
        if len(df.shape) == 2 and df.shape[1] == 1:
            df = df.ravel()
        return df

    def predict(self, X):
        """
        Prédit en appelant le modèle associé à chaque catégorie.

        @param      X   features
        @return         prédictions

        La fonction n'est pas parallélisée mais elle le pourrait.
        """
        return self._any_predict(X, 'predict')

    def decision_function(self, X):
        """
        Output of the model in case of a regressor, matrix with a score for each class and each sample
        for a classifier

        @param      X   Samples, {array-like, sparse matrix}, shape = (n_samples, n_features)
        @return         array, shape = (n_samples,.), Returns predicted values.
        """
        if hasattr(self.model, 'decision_function'):
            return self._any_predict(X, 'decision_function')
        raise NotImplementedError(
            "No decision_function for {0}".format(self.model))

    def predict_proba(self, X):
        """
        Output of the model in case of a regressor, matrix with a score for each class and each sample
        for a classifier

        @param      X   Samples, {array-like, sparse matrix}, shape = (n_samples, n_features)
        @return         array, shape = (n_samples,.), Returns predicted values.
        """
        if hasattr(self.model, 'predict_proba'):
            return self._any_predict(X, 'predict_proba')
        raise NotImplementedError(  # pragma: no cover
            "No method predict_proba for {0}".format(self.model))

    def score(self, X, y=None, sample_weight=None):
        """
        Returns the mean accuracy on the given test data and labels.

        @param      X               Training data, numpy array or sparse matrix of shape [n_samples,n_features]
        @param      y               Target values, numpy array of shape [n_samples, n_targets] (optional)
        @param      sample_weight   Weight values, numpy array of shape [n_samples, n_targets] (optional)
        @return                     score : float, Mean accuracy of self.predict(X) wrt. y.
        """
        if self._estimator_type == 'classifier':
            from sklearn.metrics import accuracy_score
            return accuracy_score(y, self.predict(X), sample_weight=sample_weight)
        if self._estimator_type == 'regressor':
            from sklearn.metrics import r2_score
            return r2_score(y, self.predict(X), sample_weight=sample_weight)
        raise RuntimeError(  # pragma: no cover
            "Unexpected estimator type '{0}', cannot guess default scoring metric.".format(
                self._estimator_type))

    ##############
    # cloning API
    ##############

    def get_params(self, deep=True):
        """
        Retourne les paramètres qui définissent l'objet
        (tous ceux nécessaires pour le cloner).

        @param      deep        unused here
        @return                 dict
        """
        res = self.P.to_dict()
        res['model'] = self.model
        if deep:
            p = self.model.get_params(deep)
            ps = {'model__{0}'.format(
                name): value for name, value in p.items()}
            res.update(ps)
        return res

    def set_params(self, **values):
        """
        Change les paramètres qui définissent l'objet
        (tous ceux nécessaires pour le cloner).

        @param      values      values
        @return                 dict
        """
        if 'model' in values:
            self.model = values['model']
            del values['model']
        elif not hasattr(self, 'model') or self.model is None:
            raise KeyError(  # pragma: no cover
                "Missing key '{0}' in [{1}]".format(
                    'model', ', '.join(sorted(values))))
        prefix = 'model__'
        ext = {k[len(prefix):]: v for k, v in values.items()
               if k.startswith(prefix)}
        self.model.set_params(**ext)
        existing = self.P.to_dict()
        ext = {k: v for k, v in values.items() if not k.startswith(prefix)}
        if ext:
            existing.update(ext)
        self.P = SkLearnParameters(**existing)
        return self

    #################
    # common methods
    #################

    def __repr__(self):
        """
        usual
        """
        return "{0}({2},{1})".format(self.__class__.__name__, repr(self.P), repr(self.model))
