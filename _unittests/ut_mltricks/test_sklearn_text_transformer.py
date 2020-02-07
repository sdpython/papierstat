"""
@brief      test log(time=2s)
"""
import unittest
import numpy
import pandas
from pyquickhelper.pycode import ExtTestCase
from sklearn.feature_extraction.text import CountVectorizer
from papierstat.mltricks import TextVectorizerTransformer


class TestSklearnTextTransformer(ExtTestCase):

    def test_text_vectorizer_transformer(self):
        X = numpy.array([["je suis", "je sais", "tu vis", "je vis"]]).T
        cvt = TextVectorizerTransformer(CountVectorizer())
        cvt.fit(X)
        z = cvt.transform(X)
        self.assertEqual(z.shape, (4, 5))
        X = pandas.DataFrame(X)
        cvt.fit(X)
        z = cvt.transform(X)
        self.assertEqual(z.shape, (4, 5))

    def test_text_vectorizer_transformer_2cols(self):
        X = numpy.array([["je suis", "je sais", "tu vis", "je vis"],
                         ["i am", "i know", "you live", "i live"]]).T
        cvt = TextVectorizerTransformer(CountVectorizer())
        cvt.fit(X)
        z = cvt.transform(X)
        self.assertEqual(z.shape, (4, 9))


if __name__ == "__main__":
    unittest.main()
