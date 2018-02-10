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
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.pipeline import make_pipeline
from src.papierstat.mltricks import SkBaseTransformLearner


class TestPipelineHelper(unittest.TestCase):

    def test_pipeline_with_two_learners(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        data = load_iris()
        X, y = data.data, data.target
        X_train, X_test, y_train, y_test = train_test_split(X, y)
        pipe = make_pipeline(SkBaseTransformLearner(LogisticRegression()),
                             DecisionTreeClassifier())
        pipe.fit(X_train, y_train)
        pred = pipe.predict(X_test)
        score = accuracy_score(y_test, pred)
        self.assertGreater(score, 0.95)


if __name__ == "__main__":
    unittest.main()
