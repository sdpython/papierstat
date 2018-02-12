# -*- coding: utf-8 -*-
"""
@file
@brief Fonctions retournant des jeux de données.
"""
import os


def get_data_folder():
    """
    Retourne le répertoire de données inclus dans ce module.
    """
    this = os.path.dirname(__file__)
    data = os.path.join(this, "data")
    return os.path.abspath(data)
