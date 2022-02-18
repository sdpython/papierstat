# -*- coding: utf-8 -*-
"""
@file
@brief Jeux de données biaisés.
"""
import numpy
from scipy.special import expit  # pylint: disable=E0611
import pandas
from sklearn.model_selection import train_test_split


__all__ = ['load_biased']


def load_biased(N=250):
    """
    Retourne un jeu de données biaisé.

    :param N: number of observations
    :return: :epkg:`pandas:DataFrame`
    """
    kids = numpy.array([0.6, 0.8, 0.9, 0.95, 1.])

    data = []
    for _ in range(0, N):
        obs = dict(
            age=numpy.random.randint(18, 65),
            gender=numpy.random.randint(0, 2),
            kids=numpy.searchsorted(kids, numpy.random.random()))
        r = 1000 + (
            expit(obs['age'] / 30.) *
            (1000 + 1000 * numpy.random.random()))
        r -= obs['kids'] * (400 + 100 * numpy.random.random())
        r -= obs['gender'] * numpy.random.randint(0, 1)
        r = max(r, 1000)
        obs['R'] = r
        data.append(obs)
    return train_test_split(pandas.DataFrame(data))
