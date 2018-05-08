# -*- coding: utf-8 -*-
"""
@file
@brief Fonctions retournant des jeux de données.
"""
from .cat import load_adult_dataset
from .carreau import load_carreau_from_zip
from .duration import duration_selling
from .enedis import load_enedis_dataset
from .geojson import get_geojson_countries
from .graph import create_tiny_graph
from .movies import load_movielens_dataset
from .search import load_search_engine_dataset
from .tweets import load_tweet_dataset
from .wines import load_wines_dataset
