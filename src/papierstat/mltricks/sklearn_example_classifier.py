"""
@file
@brief   Defines @see cl SkCustomKnn
"""
import numpy
import pandas
from mlinsights.sklapi import SkBaseClassifier, SkException


class SkCustomKnn(SkBaseClassifier):
    """
    Implements the `k-Nearest Neighbors <http://en.wikipedia.org/
    wiki/K-nearest_neighbors_algorithm>`_ as an example.
    """

    def __init__(self, k=1):
        """
        constructor

        @param      k       number of neighbors to considers
        """
        SkBaseClassifier.__init__(self, k=k)

    def fit(self, X, y=None, sample_weight=None):
        """
        Train a k-NN model. There is not much to do except storing the training
        examples.

        @param      X               Training data, numpy array or sparse matrix of
                                    shape [n_samples,n_features]
        @param      y               Target values, numpy array of shape
                                    [n_samples, n_targets] (optional)
        @param      sample_weight   Weight values, numpy array of shape
                                    [n_samples, n_targets] (optional)
        @return                     self : returns an instance of self.
        """
        if sample_weight is not None:
            raise NotImplementedError(  # pragma: no cover
                "sample_weight must be None")
        if len(X) < self.P.k:
            raise SkException(  # pragma: no cover
                f"number of samples cannot be smaller than k={self.P.k}")
        if isinstance(X, pandas.DataFrame):
            X = X.asmatrix()
        if isinstance(y, pandas.DataFrame):
            y = y.asmatrix()
        if len(X) != len(y):
            raise SkException(  # pragma: no cover
                f"X and y should have the same dimension not: {len(X)} != {len(y)}")
        if min(y) < 0:
            raise SkException(  # pragma: no cover
                "class should be positive or null integer")
        self._TrainingX = X
        self._Trainingy = y
        self._nbclass = max(y) + 1
        return self

    def predict(self, X):
        """
        Predicts, usually, it calls the
        :meth:`decision_function <papierstat.mltricks.sklearn_example_classifier.
        SkCustomKnn.decision_function>` method.

        @param      X   Samples, {array-like, sparse matrix},
                        shape = (n_samples, n_features)
        @return         self : returns an instance of self.
        """
        scores = self.decision_function(X)
        if len(scores.shape) == 1:
            indices = (scores > 0).astype(numpy.int)
        else:
            indices = scores.argmax(axis=1)
        return indices

    def decision_function(self, X):
        """
        Computes the output of the model in case of a regressor,
        matrix with a score for each class and each sample
        for a classifier.

        @param      X   Samples, {array-like, sparse matrix},
                        *shape = (n_samples, n_features)*
        @return         array, shape = (n_samples,.), Returns predicted values.
        """
        nb = len(X)
        res = [self.knn_search(X[i, :]) for i in range(0, nb)]
        y = self._Trainingy
        res = [[el + (y[el[-1]],) for el in m] for m in res]
        mk = numpy.zeros((len(X), self._nbclass))
        for i, row in enumerate(res):
            for el in row:
                w = self.distance2weight(el[0])
                mk[i, el[-1]] += w
        return mk

    ##################
    # private methods
    ##################

    def distance2weight(self, d):
        """
        Converts a distance to weight.

        @param      d       distance
        @return             weight (1/(d+1))
        """
        return 1.0 / (1.0 + d)

    def knn_search(self, x):
        """
        Finds the  *k* nearest neighbors for x.

        @param      x       vector
        @return             k-nearest neighbors list( (distance**2, index) )
        """
        X = self._TrainingX
        ones = numpy.ones((len(X), len(x)))
        po = x * ones
        X_x = X - po
        prod = sorted([((X_x[i, :] ** 2).sum(), i) for i in range(0, len(X))])
        return prod[:self.P.k]
