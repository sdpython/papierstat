"""
@brief      test log(time=2s)
"""

import sys
import os
import unittest
import numpy
import scipy.sparse
import pandas
import pickle
from io import BytesIO


try:
    import src
except ImportError:
    path = os.path.normpath(
        os.path.abspath(
            os.path.join(
                os.path.split(__file__)[0],
                "..",
                "..")))
    if path not in sys.path:
        sys.path.append(path)
    import src

try:
    import pyquickhelper as skip_
except ImportError:
    path = os.path.normpath(
        os.path.abspath(
            os.path.join(
                os.path.split(__file__)[0],
                "..",
                "..",
                "..",
                "pyquickhelper",
                "src")))
    if path not in sys.path:
        sys.path.append(path)
    import pyquickhelper as skip_

from pyquickhelper.pycode import ExtTestCase
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import GridSearchCV

from src.papierstat.mltricks.kmeans_constraint_ import linearize_matrix
from src.papierstat.mltricks import ConstraintKMeans


class TestSklearnConstraintKMeans(ExtTestCase):

    def test_mat_lin(self):
        mat = numpy.identity(3)
        lin = linearize_matrix(mat)
        exp = numpy.array([[1., 0., 0.],
                           [0., 0., 1.],
                           [0., 0., 2.],
                           [0., 1., 0.],
                           [1., 1., 1.],
                           [0., 1., 2.],
                           [0., 2., 0.],
                           [0., 2., 1.],
                           [1., 2., 2.]])
        self.assertEqual(exp, lin)

    def test_mat_lin_sparse(self):
        mat = numpy.identity(3)
        mat[0, 2] = 8
        mat[1, 2] = 5
        mat[2, 1] = 7
        mat = scipy.sparse.csr_matrix(mat)
        lin = linearize_matrix(mat)
        exp = numpy.array([[1., 0., 0.],
                           [8., 0., 2.],
                           [1., 1., 1.],
                           [5., 1., 2.],
                           [7., 2., 1.],
                           [1., 2., 2.]])
        self.assertEqual(exp, lin)

    def test_mat_lin_sparse2(self):
        mat = numpy.identity(3)
        mat[0, 1] = 8
        mat[1, 1] = 0
        mat[2, 1] = 7
        mat = scipy.sparse.csr_matrix(mat)
        lin = linearize_matrix(mat)
        exp = numpy.array([[1., 0., 0.],
                           [8., 0., 1.],
                           [7., 2., 1.],
                           [1., 2., 2.]])
        self.assertEqual(exp, lin)

    def test_mat_lin_sparse3(self):
        mat = numpy.identity(3)
        mat[0, 1] = 8
        mat[2, 1] = 7
        mat = scipy.sparse.csr_matrix(mat)
        lin = linearize_matrix(mat)
        exp = numpy.array([[1., 0., 0.],
                           [8., 0., 1.],
                           [1., 1., 1.],
                           [7., 2., 1.],
                           [1., 2., 2.]])
        self.assertEqual(exp, lin)

    def test_mat_sort(self):
        mat = numpy.identity(3)
        mat[2, 0] = 0.3
        mat[1, 0] = 0.2
        mat[0, 0] = 0.1
        exp = numpy.array([[0.1, 0., 0.], [0.2, 1., 0.], [0.3, 0., 1.]])
        sort = mat[mat[:, 0].argsort()]
        self.assertEqual(exp, sort)
        mat.sort(axis=0)
        self.assertNotEqual(exp, mat)
        mat.sort(axis=1)
        self.assertNotEqual(exp, mat)

    def test_kmeans_constraint(self):
        mat = numpy.array([[0, 0], [0.2, 0.2], [-0.1, -0.1], [1, 1]])
        km = ConstraintKMeans(n_clusters=2, verbose=0)
        km.fit(mat)
        self.assertEqual(km.cluster_centers_.shape, (2, 2))
        self.assertEqualFloat(km.inertia_, 0.455)
        if km.labels_[0] == 0:
            self.assertEqual(km.labels_, numpy.array([0, 1, 0, 1]))
            self.assertEqual(km.cluster_centers_, numpy.array(
                [[-0.05, -0.05], [0.6, 0.6]]))
        else:
            self.assertEqual(km.labels_, numpy.array([1, 0, 1, 0]))
            self.assertEqual(km.cluster_centers_, numpy.array(
                [[0.6, 0.6], [-0.05, -0.05]]))
        pred = km.predict(mat)
        if km.labels_[0] == 0:
            self.assertEqual(pred, numpy.array([0, 0, 0, 1]))
        else:
            self.assertEqual(pred, numpy.array([1, 1, 1, 0]))

    def test_kmeans_constraint_sparse(self):
        mat = numpy.array([[0, 0], [0.2, 0.2], [-0.1, -0.1], [1, 1]])
        mat = scipy.sparse.csr_matrix(mat)
        km = ConstraintKMeans(n_clusters=2, verbose=0)
        km.fit(mat)
        self.assertEqual(km.cluster_centers_.shape, (2, 2))
        self.assertEqualFloat(km.inertia_, 0.455)
        if km.labels_[0] == 0:
            self.assertEqual(km.labels_, numpy.array([0, 1, 0, 1]))
            self.assertEqual(km.cluster_centers_, numpy.array(
                [[-0.05, -0.05], [0.6, 0.6]]))
        else:
            self.assertEqual(km.labels_, numpy.array([1, 0, 1, 0]))
            self.assertEqual(km.cluster_centers_, numpy.array(
                [[0.6, 0.6], [-0.05, -0.05]]))
        pred = km.predict(mat)
        if km.labels_[0] == 0:
            self.assertEqual(pred, numpy.array([0, 0, 0, 1]))
        else:
            self.assertEqual(pred, numpy.array([1, 1, 1, 0]))

    def test_kmeans_constraint_pipeline(self):
        data = load_iris()
        X, y = data.data, data.target
        X_train, X_test, y_train, y_test = train_test_split(X, y)
        km = ConstraintKMeans()
        pipe = make_pipeline(km, LogisticRegression())
        pipe.fit(X_train, y_train)
        pred = pipe.predict(X_test)
        score = accuracy_score(y_test, pred)
        self.assertGreater(score, 0.8)
        score2 = pipe.score(X_test, y_test)
        self.assertEqual(score, score2)
        rp = repr(km)
        self.assertStartsWith(
            "ConstraintKMeans(algorithm='auto', copy_x=True, init='k-means++'", rp)

    def test_kmeans_constraint_grid(self):
        df = pandas.DataFrame(dict(y=[0, 1, 0, 1, 0, 1, 0, 1],
                                   X1=[0.5, 0.6, 0.52, 0.62,
                                       0.5, 0.6, 0.51, 0.61],
                                   X2=[0.5, 0.6, 0.7, 0.5, 1.5, 1.6, 1.7, 1.8]))
        X = df.drop('y', axis=1)
        y = df['y']
        model = make_pipeline(ConstraintKMeans(), DecisionTreeClassifier())
        res = model.get_params(True)
        self.assertNotEmpty(res)

        parameters = {
            'constraintkmeans__n_clusters': [2, 3, 4]}
        clf = GridSearchCV(model, parameters)
        clf.fit(X, y)
        pred = clf.predict(X)
        self.assertEqualArray(y, pred)

    def test_kmeans_constraint_pickle(self):
        df = pandas.DataFrame(dict(y=[0, 1, 0, 1, 0, 1, 0, 1],
                                   X1=[0.5, 0.6, 0.52, 0.62,
                                       0.5, 0.6, 0.51, 0.61],
                                   X2=[0.5, 0.6, 0.7, 0.5, 1.5, 1.6, 1.7, 1.8]))
        X = df.drop('y', axis=1)
        y = df['y']
        model = ConstraintKMeans(n_clusters=2)
        model.fit(X, y)
        pred = model.transform(X)
        st = BytesIO()
        pickle.dump(model, st)
        st = BytesIO(st.getvalue())
        rec = pickle.load(st)
        pred2 = rec.transform(X)
        self.assertEqualArray(pred, pred2)


if __name__ == "__main__":
    unittest.main()
