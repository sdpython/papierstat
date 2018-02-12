"""
@brief      test log(time=2s)
"""

import sys
import os
import unittest


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
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.metrics import accuracy_score
from sklearn.pipeline import make_pipeline
from src.papierstat.mltricks import SkBaseTransformStacking


class TestSklearnStacking(ExtTestCase):

    def test_pipeline_with_two_classifiers(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        data = load_iris()
        X, y = data.data, data.target
        X_train, X_test, y_train, y_test = train_test_split(X, y)
        conv = SkBaseTransformStacking(
            [LogisticRegression(), DecisionTreeClassifier()])
        pipe = make_pipeline(conv, DecisionTreeClassifier())
        pipe.fit(X_train, y_train)
        pred = pipe.predict(X_test)
        score = accuracy_score(y_test, pred)
        self.assertGreater(score, 0.8)
        score2 = pipe.score(X_test, y_test)
        self.assertEqual(score, score2)
        rp = repr(conv)
        self.assertStartsWith(
            'SkBaseTransformStacking([LogisticRegression(C=1.0, class_weight=None,', rp)

    def test_pipeline_with_params(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        data = load_iris()
        X, y = data.data, data.target
        X_train, X_test, y_train, y_test = train_test_split(X, y)
        conv = SkBaseTransformStacking([LinearRegression(normalize=True),
                                        DecisionTreeClassifier(max_depth=3)])
        pipe = make_pipeline(conv, DecisionTreeRegressor())
        pars = pipe.get_params(deep=True)
        self.assertIn(
            'skbasetransformstacking__estimator_0__estimator__fit_intercept', pars)
        self.assertEqual(
            pars['skbasetransformstacking__estimator_0__estimator__normalize'], True)
        conv = SkBaseTransformStacking([LinearRegression(normalize=False),
                                        DecisionTreeClassifier(max_depth=2)])
        pipe = make_pipeline(conv, DecisionTreeRegressor())
        pipe.set_params(**pars)
        pars = pipe.get_params()
        self.assertIn(
            'skbasetransformstacking__estimator_0__estimator__fit_intercept', pars)
        self.assertEqual(
            pars['skbasetransformstacking__estimator_0__estimator__normalize'], True)


if __name__ == "__main__":
    unittest.main()
