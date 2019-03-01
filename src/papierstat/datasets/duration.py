# -*- coding: utf-8 -*-
"""
@file
@brief Jeux de données artificiel lié à la prédiction de durées.
"""
from datetime import datetime, timedelta
import pandas
from numpy.random import randn, rand, gamma


def duration_selling(date_begin=None, date_end=None,
                     mean_per_day=10, sigma_per_day=5,
                     week_pattern=None,
                     hour_begin=9, hour_end=19,
                     gamma_k=6., gamma_theta=0.25):
    """
    Construit un jeu de données artificiel qui simule des paquets
    préparés par un magasin. Chaque paquet est préparé dès la réception
    d'une commande à une heure précise, il est ensuite stocké
    jusqu'à ce qu'un client viennent le chercher.

    @param      date_begin      première date
    @param      date_end        dernière date
    @param      hour_begin      heure d'ouverture du magasin
    @param      hour_end        heure de fermeture du magasin
    @param      week_pattern    tableau de 7 valeurs ou None
                                pour une distribution uniforme sur les jours
                                de la semaine
    @param      mean_per_day    nombre de paquets moyen par jour (suit une loi gaussienne)
    @param      sigma_per_day   écart type pour la loi gaussienne
    @param      gamma_k         paramètre *k* d'une loi gamma
    @param      gamma_theta     paramètre :math:`\\theta` d'une loi gamma
    @return                     jeu de données

    .. runpython::
        :showcode:

        from papierstat.datasets.duration import duration_selling
        print(duration_selling().head())

    Les commandes sont réparties de façon uniformes sur la journée
    même si c'est peu probable. La durée suit une loi :math:`\\Gamma`.
    Cette durée est ajoutée à l'heure où est passée la commande,
    les heures nocturnes et le week-end ne sont pas comptées.
    La durée ne peut excéder 10h.

    .. runpython::
        :rst:

        from papierstat.datasets.documentation import list_notebooks_rst_links
        links = list_notebooks_rst_links('lectures', 'artificiel_duration')
        links = ['    * %s' % s for s in links]
        print('\\n'.join(links))
    """
    if date_begin is None:
        date_begin = datetime.now() - timedelta(365, 1, 1)
        date_begin = datetime(
            date_begin.year, date_begin.month, date_begin.day)
    if date_end is None:
        date_end = datetime.now()
        date_end = datetime(date_end.year, date_end.month, date_end.day)
    if date_begin >= date_end:
        raise ValueError(
            "begin >= end {0} >= {1}".format(date_begin, date_end))
    if week_pattern is None:
        week_pattern = [1.] * 5 + [0., 0.]

    gauss = randn(1000)
    pos_gauss = 0
    uni = rand(1000)
    pos_uni = 0
    gam = gamma(gamma_k, gamma_theta, 1000)
    pos_gam = 0
    add1d = timedelta(seconds=24 * 3600) - \
        (timedelta(seconds=hour_end * 3600) - timedelta(seconds=hour_begin * 3600))

    day_duration = (hour_end - hour_begin) * 3600
    date_begin += timedelta(seconds=hour_begin * 3600)

    rows = []
    while date_begin <= date_end:
        wk = date_begin.weekday()
        nb = max(int(week_pattern[wk] * mean_per_day), 0)
        if nb == 0:
            date_begin += timedelta(days=1)
            continue
        nb += gauss[pos_gauss] * sigma_per_day  # pylint: disable=E1136
        nb = int(max(nb, 0))
        pos_gauss += 1
        if pos_gauss >= len(gauss):
            gauss = randn(1000)
            pos_gauss = 0
        if nb == 0:
            date_begin += timedelta(days=1)
            continue
        for _ in range(0, int(nb)):
            db = uni[pos_uni] * day_duration  # pylint: disable=E1136
            pos_uni += 1
            if pos_uni >= len(uni):
                uni = rand(1000)
                pos_uni = 0

            g = min(gam[pos_gam] * 3600, 36000)  # pylint: disable=E1136
            pos_gam += 1
            if pos_gam >= len(gam):
                gam = gamma(gamma_k, gamma_theta, 1000)
                pos_gam = 0

            rec = dict(commande=date_begin + timedelta(seconds=db))
            rec['true_duration'] = g / 3600
            end = rec['commande'] + timedelta(seconds=g)
            if end.hour >= hour_end or end.hour < hour_begin:
                end += add1d
                while end.weekday() >= 5:
                    end += timedelta(seconds=24 * 3600)
            rec["reception"] = end
            rows.append(rec)
        date_begin += timedelta(days=1)
    return pandas.DataFrame(rows)
