# -*- coding: utf-8 -*-
"""
@file
@brief Automatatisation de certaines parties de la documentation.
"""
import os


def list_notebooks(subfolder, name=None, contains=None):
    """
    Retourne les notebooks qui contiennent *name* dans leur nom.

    @param      subfolder   sous-répertoire où chercher
    @param      name        préfixe à chercher
    @param      contains    extrait à chercher
    @return                 liste des notebooks (sans répertoire)
    """
    this = os.path.dirname(__file__)
    nbs = [os.path.abspath(
        os.path.normpath(
            os.path.join(
                this, '..', '..', '..', '..', 'notebooks', subfolder))),
           os.path.abspath(
        os.path.normpath(
            os.path.join(
                this, '..', '..', '..', '_doc', 'notebooks', subfolder)))]
    nb_ = list(filter(os.path.exists, nbs))
    if len(nb_) == 0:
        raise FileNotFoundError(  # pragma: no cover
            "Unable to find notebooks in\n{0}".format('\n'.join(nbs)))
    nb = nb_[0]

    name_ = name
    if name is not None:
        names = [_ for _ in os.listdir(nb) if _.startswith(name_)]
    if contains is not None:
        names = [_ for _ in os.listdir(nb) if contains in _]
    if len(names) == 0:
        raise FileNotFoundError(  # pragma: no cover
            "Unable to find any notebook in '{0}'.".format(nb))
    return names


def list_notebooks_rst_links(subfolder, name=None, contains=None):
    """
    Retourne une liste de notebooks au format :epkg:`rst`.

    @param      subfolder   sous-répertoire où chercher
    @param      name        préfixe à chercher
    @param      contains    extrait à chercher
    @return                 liste des liens
    """
    names = list_notebooks(subfolder, name, contains)
    return [':ref:`{0}rst`'.format(
        os.path.splitext(os.path.split(name)[1])[0].replace('_', ''))
        for name in names]
