"""
@brief      test log(time=2s)
"""

import sys
import os
from io import BytesIO
import pickle
import unittest
import pandas


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

from pyquickhelper.loghelper import fLOG
from pyquickhelper.pycode import ExtTestCase
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from src.papierstat.datasets import load_wines_dataset
from src.papierstat.mltricks import SkBaseLearnerCategory


class TestSklearnCategory(ExtTestCase):

    def test_fit_cat(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        df = pandas.DataFrame(dict(y=[0, 1, 0, 1, 0, 1, 0, 1],
                                   X1=[0.5, 0.6, 0.52, 0.62,
                                       0.5, 0.6, 0.51, 0.61],
                                   X2=[0.5, 0.6, 0.7, 0.5, 1.5, 1.6, 1.7, 1.8],
                                   cat=['red', 'red', 'blue', 'blue', 'red', 'red', 'red', 'blue']))
        X = df.drop('y', axis=1)
        y = df['y']
        model = SkBaseLearnerCategory('cat', DecisionTreeClassifier())
        model.fit(X, y)
        pred = model.predict(X)
        self.assertGreater(len(pred), 0)
        self.assertEqualArray(y, pred)

    def test_fit_cat_array(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        df = pandas.DataFrame(dict(y=[0, 1, 0, 1, 0, 1, 0, 1],
                                   X1=[0.5, 0.6, 0.52, 0.62,
                                       0.5, 0.6, 0.51, 0.61],
                                   X2=[0.5, 0.6, 0.7, 0.5, 1.5, 1.6, 1.7, 1.8],
                                   cat=[9, 10, 9, 10, 9, 10, 9, 10]))
        X = df.drop('y', axis=1)
        y = df['y']
        model = SkBaseLearnerCategory('cat', DecisionTreeClassifier())
        model.fit(X, y)
        pred = model.predict(X)
        self.assertGreater(len(pred), 0)
        self.assertEqualArray(y, pred)

    def test_fit_predict(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        df = pandas.DataFrame(dict(y=[0, 1, 0, 1, 0, 1, 0, 1],
                                   X1=[0.5, 0.6, 0.52, 0.62,
                                       0.5, 0.6, 0.51, 0.61],
                                   X2=[0.5, 0.6, 0.7, 0.5, 1.5, 1.6, 1.7, 1.8],
                                   cat=['red', 'red', 'blue', 'blue', 'red', 'red', 'red', 'blue']))
        X = df.drop('y', axis=1)
        y = df['y']
        model = SkBaseLearnerCategory('cat', DecisionTreeClassifier())
        model.fit(X, y)

        pred = model.predict(X)
        self.assertGreater(len(pred), 0)
        self.assertEqualArray(y, pred)

        pred = model.score(X, y)
        self.assertGreater(pred, 0)

        pred = model.predict_proba(X)
        self.assertGreater(len(pred), 0)
        self.assertEqualArray(y, pred[:, 1])
        self.assertRaise(lambda: model.decision_function(X),
                         NotImplementedError)

    def test_pickle(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        df = pandas.DataFrame(dict(y=[0, 1, 0, 1, 0, 1, 0, 1],
                                   X1=[0.5, 0.6, 0.52, 0.62,
                                       0.5, 0.6, 0.51, 0.61],
                                   X2=[0.5, 0.6, 0.7, 0.5, 1.5, 1.6, 1.7, 1.8],
                                   cat=['red', 'red', 'blue', 'blue', 'red', 'red', 'red', 'blue']))
        X = df.drop('y', axis=1)
        y = df['y']
        model = SkBaseLearnerCategory('cat', DecisionTreeClassifier())
        model.fit(X, y)

        pred = model.predict(X)

        st = BytesIO()
        pickle.dump(model, st)
        st = BytesIO(st.getvalue())
        rec = pickle.load(st)
        pred2 = rec.predict(X)
        self.assertEqualArray(pred, pred2)

    def test_grid(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        df = pandas.DataFrame(dict(y=[0, 1, 0, 1, 0, 1, 0, 1],
                                   X1=[0.5, 0.6, 0.52, 0.62,
                                       0.5, 0.6, 0.51, 0.61],
                                   X2=[0.5, 0.6, 0.7, 0.5, 1.5, 1.6, 1.7, 1.8],
                                   cat=['red', 'red', 'blue', 'blue', 'red', 'red', 'red', 'blue']))
        X = df.drop('y', axis=1)
        y = df['y']
        model = SkBaseLearnerCategory('cat', DecisionTreeClassifier())
        res = model.get_params(True)
        del res['model']
        self.assertEqual(res, {'colnameind': 'cat', 'model__class_weight': None,
                               'model__criterion': 'gini', 'model__max_depth': None,
                               'model__max_features': None, 'model__max_leaf_nodes': None,
                               'model__min_impurity_decrease': 0.0, 'model__min_impurity_split': None, 'model__min_samples_leaf': 1,
                               'model__min_samples_split': 2, 'model__min_weight_fraction_leaf': 0.0,
                               'model__presort': False, 'model__random_state': None, 'model__splitter': 'best'})

        parameters = {'model__max_depth': [2, 3]}
        clf = GridSearchCV(model, parameters)
        clf.fit(X, y)

        pred = clf.predict(X)
        self.assertEqualArray(y, pred)

    def test_wines(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        df = load_wines_dataset()

        X = df.drop(['quality', 'color'], axis=1)
        X = X[['alcohol', 'volatile_acidity', 'density']]
        y = df['quality']
        color = df['color']

        X_train, X_test, y_train, y_test, color_train, color_test = train_test_split(
            X, y, color)

        model = SkBaseLearnerCategory("color", LogisticRegression())
        new_x_train = pandas.concat([X_train, color_train], axis=1)
        model.fit(new_x_train, y_train)
        new_x_test = pandas.concat([X_test, color_test], axis=1)
        acc1 = accuracy_score(y_test, model.predict(new_x_test))

        self.assertNotEqualDataFrame(model.models['red'].coef_,
                                     model.models['white'].coef_)

        clr = LogisticRegression()
        clr.fit(X_train, y_train)
        acc2 = accuracy_score(y_test, clr.predict(X_test))
        self.assertGreater(acc1, 0.45)
        self.assertGreater(acc2, 0.45)
        self.assertGreater(acc1, acc2 * 0.999)


if __name__ == "__main__":
    unittest.main()
