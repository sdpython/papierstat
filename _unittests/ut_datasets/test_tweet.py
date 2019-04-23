# -*- coding: utf-8 -*-
"""
@brief      test log(time=13s)
"""
import unittest
from pyquickhelper.pycode import ExtTestCase, get_temp_folder
from papierstat.datasets import load_tweet_dataset


class TestTweet(ExtTestCase):

    def test_tweets(self):
        temp = get_temp_folder(__file__, "temp_tweets")
        df = load_tweet_dataset(cache=temp)
        self.assertEqual(df.shape, (5088, 20))


if __name__ == "__main__":
    unittest.main()
