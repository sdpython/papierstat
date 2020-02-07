"""
@file
@brief Implements TextVectorizerTransformer.
"""
import numpy
from scipy import sparse
import pandas
from sklearn.base import BaseEstimator, TransformerMixin, clone


class TextVectorizerTransformer(BaseEstimator, TransformerMixin):
    """
    Overwrites *TfIdfVectorizer* or *CountVectorizer*
    so that it can be used in a pipeline.

    Parameters
    ----------

    estimator: estimator to fit on every column

    estimators_: trained estimators, one per column
    """

    def __init__(self, estimator):
        """
        @param      estimator       *TfIdfVectorizer* or *CountVectorizer*
        """
        self.estimator = estimator

    def fit(self, X, y=None):
        """
        Trains an estimator on every column.
        """
        self.estimators_ = []
        for i in range(X.shape[1]):
            est = clone(self.estimator)
            if isinstance(X, pandas.DataFrame):
                col = X.iloc[:, i]
            elif isinstance(X, numpy.ndarray):
                col = X[:, i]
            else:
                raise TypeError("X must be an array or a dataframe.")
            est.fit(col)
            self.estimators_.append(est)
        return self

    def transform(self, X):
        """
        Applies the vectorizer on X.
        """
        if len(self.estimators_) != X.shape[1]:
            raise ValueError("Unexpected number of columns {}, expecting {}".format(
                X.shape[1], len(self.estimators_)))
        res = []
        for i in range(X.shape[1]):
            if isinstance(X, pandas.DataFrame):
                col = X.iloc[:, i]
            elif isinstance(X, numpy.ndarray):
                col = X[:, i]
            else:
                raise TypeError("X must be an array or a dataframe.")
            r = self.estimators_[i].transform(col)
            res.append(r)
        if len(res) == 1:
            return res[0]
        if all(map(lambda r: isinstance(r, numpy.ndarray), res)):
            return numpy.hstack(res)
        return sparse.hstack(res)
