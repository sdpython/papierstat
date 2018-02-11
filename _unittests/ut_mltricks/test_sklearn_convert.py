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
from sklearn.metrics import accuracy_score, r2_score
from sklearn.pipeline import make_pipeline
from src.papierstat.mltricks import SkBaseTransformLearner


class TestPipelineHelper(ExtTestCase):

    def test_pipeline_with_two_classifiers(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        data = load_iris()
        X, y = data.data, data.target
        X_train, X_test, y_train, y_test = train_test_split(X, y)
        conv = SkBaseTransformLearner(LogisticRegression())
        pipe = make_pipeline(conv, DecisionTreeClassifier())
        pipe.fit(X_train, y_train)
        pred = pipe.predict(X_test)
        score = accuracy_score(y_test, pred)
        self.assertGreater(score, 0.8)
        score2 = pipe.score(X_test, y_test)
        self.assertEqual(score, score2)
        rp = repr(conv)
        self.assertStartsWith(
            'SkBaseTransformLearner(model=LogisticRegression(C=1.0,', rp)

    def test_pipeline_with_callable(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        data = load_iris()
        X, y = data.data, data.target
        X_train, X_test, y_train, y_test = train_test_split(X, y)
        tmod = LogisticRegression()
        conv = SkBaseTransformLearner(tmod, method=tmod.decision_function)
        pipe = make_pipeline(conv, DecisionTreeClassifier())
        pipe.fit(X_train, y_train)
        pred = pipe.predict(X_test)
        score = accuracy_score(y_test, pred)
        self.assertGreater(score, 0.8)
        score2 = pipe.score(X_test, y_test)
        self.assertEqual(score, score2)
        rp = repr(conv)
        self.assertStartsWith(
            'SkBaseTransformLearner(model=LogisticRegression(C=1.0,', rp)

    def test_pipeline_with_two_regressors(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        data = load_iris()
        X, y = data.data, data.target
        X_train, X_test, y_train, y_test = train_test_split(X, y)
        conv = SkBaseTransformLearner(LinearRegression())
        pipe = make_pipeline(conv, DecisionTreeRegressor())
        pipe.fit(X_train, y_train)
        pred = pipe.predict(X_test)
        score = r2_score(y_test, pred)
        self.assertLesser(score, 1.)
        score2 = pipe.score(X_test, y_test)
        self.assertEqual(score, score2)
        rp = repr(conv)
        self.assertStartsWith(
            'SkBaseTransformLearner(model=LinearRegression(copy_X=True,', rp)


if __name__ == "__main__":
    unittest.main()
