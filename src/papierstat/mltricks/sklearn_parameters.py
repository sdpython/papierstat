# -*- coding: utf-8 -*-
"""
@file
@brief Defines @see cl SkLearnParameters
"""
import textwrap


class SkException (Exception):

    """
    custom exception
    """
    pass


class SkLearnParameters:

    """
    Définit une classe pour des paramètres associés à un learner de :epkg:`scikit-learn`.
    """

    def __init__(self, **kwargs):
        """
        Stocke les paramètres dans la classe elle-même.
        """
        self._keys = list(kwargs.keys())
        for k, v in kwargs.items():
            self.validate(k, v)
            setattr(self, k, v)

    def validate(self, name, value):
        """
        Valide un paramètre et sa valuer.

        @param  name        nom
        @param  value       valuer
        @raises             jette @see cl SkException en cas d'erreur
        """
        if name.startswith("_") or name.endswith("_"):
            raise SkException(
                "Le nom d'un paramètre ne peut commencer ou se terminer par '_' : {0}".format(name))

    @property
    def Keys(self):
        """
        Retourne les noms des paramètres.
        """
        return self._keys

    def __repr__(self):
        """
        classique
        """
        def fmt(v):
            if isinstance(v, str):
                return "'{0}'".format(v)
            else:
                return repr(v)
        text = ", ".join("{0}={1}".format(k, fmt(getattr(self, k)))
                         for k in sorted(self.Keys))
        return "\n".join(textwrap.wrap(text, subsequent_indent="    "))

    def to_dict(self):
        """
        Retourne les paramètres sous la forme d'un dictionnaire.

        @return         dict
        """
        return {k: getattr(self, k) for k in self.Keys}
