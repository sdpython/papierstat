# -*- coding: utf-8 -*-
"""
@file
@brief Automatatisation de certaines parties de la documentation.
"""
import os


def list_notebooks(subfolder, name):
    """
    Retourne les notebooks qui contiennent *name* dans leur nom.

    @param      subfolder   sous-répertoire où chercher
    @param      name        nom à chercher
    @return                 liste des notebooks (sans répertoire)
    """
    this = os.path.dirname(__file__)
    nbs = [os.path.abspath(os.path.normpath(os.path.join(this, '..', '..', '..', '..',
                                                         'notebooks', subfolder))),
           os.path.abspath(os.path.normpath(os.path.join(this, '..', '..', '..',
                                                         '_doc', 'notebooks', subfolder)))]
    nb_ = list(filter(os.path.exists, nbs))
    if len(nb_) == 0:
        raise FileNotFoundError(
            "Unable to find notebooks in\n{0}".format('\n'.join(nbs)))
    nb = nb_[0]

    name_ = name
    names = [_ for _ in os.listdir(nb) if _.startswith(name_)]
    if len(names) == 0:
        raise FileNotFoundError(
            "Unable to find any notebook in '{0}'.".format(nb))
    return names


def list_notebooks_rst_links(subfolder, name):
    """
    Retourne une liste de notebooks au format :epkg:`rst`.

    @param      subfolder   sous-répertoire où chercher
    @param      name        nom à chercher
    @return                 liste des liens
    """
    names = list_notebooks(subfolder, name)
    return [':ref:`{0}rst`'.format(os.path.splitext(os.path.split(name)[1])[0].replace('_', '')) for name in names]
