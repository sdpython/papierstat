# -*- coding: utf-8 -*-
"""
@file
@brief Jeux de données reliés aux données carroyées.
"""
import os
import zipfile
import collections
import datetime
import tempfile
from io import BytesIO
from dbfread.field_parser import FieldParser
from dbfread import DBF
from dbfread.dbf import expand_year
import pandas
from geopandas import GeoDataFrame
from .data_helper import get_data_folder


class MyDBF(DBF):
    """
    Overwrites `DBF <https://github.com/olemb/dbfread/blob/master/dbfread/dbf.py#L77>`_
    to read data from memory and not from a file.
    """

    def __init__(self, filename, encoding=None, ignorecase=True,
                 lowernames=False, parserclass=FieldParser,
                 recfactory=collections.OrderedDict,
                 load=False, raw=False, ignore_missing_memofile=False,
                 char_decode_errors='strict'):

        if isinstance(filename, str):
            DBF.__init__(self, filename, encoding=encoding, ignorecase=ignorecase,
                         lowernames=lowernames, parserclass=parserclass,
                         recfactory=recfactory, load=load,
                         raw=raw, ignore_missing_memofile=ignore_missing_memofile,
                         char_decode_errors=char_decode_errors)
        else:
            self.encoding = encoding
            self.ignorecase = ignorecase
            self.lowernames = lowernames
            self.parserclass = parserclass
            self.raw = raw
            self.ignore_missing_memofile = ignore_missing_memofile
            self.char_decode_errors = char_decode_errors

            if recfactory is None:
                self.recfactory = lambda items: items
            else:
                self.recfactory = recfactory

            self.name = None
            self.filename = None
            self.content = filename

            self._records = None
            self._deleted = None

            # Filled in by self._read_headers()
            self.memofilename = None
            self.header = None
            self.fields = []       # namedtuples
            self.field_names = []  # strings

            obj = BytesIO(filename)
            self._read_header(obj)
            self._read_field_headers(obj)
            self._check_headers()

            try:
                self.date = datetime.date(expand_year(self.header.year),
                                          self.header.month, self.header.day)
            except ValueError:
                # Invalid date or '\x00\x00\x00'.
                self.date = None

            self.memofilename = self._get_memofilename()

            if load:
                self.load()

    def _iter_records(self, record_type=b' '):
        infile = BytesIO(self.content)
        with self._open_memofile() as memofile:

            # Skip to first record.
            infile.seek(self.header.headerlen, 0)

            if not self.raw:
                field_parser = self.parserclass(self, memofile)
                parse = field_parser.parse

            # Shortcuts for speed.
            skip_record = self._skip_record
            read = infile.read

            while True:
                sep = read(1)

                if sep == record_type:
                    if self.raw:
                        items = [(field.name, read(field.length))
                                 for field in self.fields]
                    else:
                        items = [(field.name,
                                  parse(field, read(field.length)))
                                 for field in self.fields]

                    yield self.recfactory(items)

                elif sep in (b'\x1a', b''):
                    # End of records.
                    break
                else:
                    skip_record(infile)


def load_dbf_from_zip(filename):
    """
    Loads a *.dbf* file compressed into a zip file.
    It only takes the first *.dbf* file from the zip.

    @param      filename    zip file
    @return                 dataframe
    """
    with zipfile.ZipFile(filename) as myzip:
        names0 = myzip.infolist()
        names = [_.filename for _ in names0 if _.filename.endswith(".dbf")]
        if len(names) == 0:
            raise FileNotFoundError("No dbf file in '{0}'".format(filename))
        with myzip.open(names[0], "r") as f:
            content = f.read()
    data = list(MyDBF(content))
    return pandas.DataFrame(data)


def _read_geopandas_from_bytes(mif, mid, **kwargs):
    """
    Returns a GeoDataFrame from two sequences of bytes,
    one for file *.mif*, one from file *.mid*.
    Unfortunately, :epkg:`geopandas` does not read from
    a buffer, and :epkg:`fiona` does it after writing
    in a virtual file (not clear if it is a temporary file or not).
    """
    with tempfile.NamedTemporaryFile(mode='w+b', delete=False, suffix='.mif') as temp:
        temp.write(mif)
        name_mif = temp.name
        name_mid = temp.name.replace(".mif", ".mid")
        with open(name_mid, "wb") as f:
            f.write(mid)
    gdf = GeoDataFrame.from_file(name_mid, **kwargs)
    if os.path.exists(name_mid):
        os.remove(name_mid)
    if os.path.exists(name_mif):
        os.remove(name_mif)
    return gdf


def load_shapes_from_zip(filename):
    """
    Loads a *.mif* and a *.mid* file compressed into a zip file.
    It only takes the first *.mid* and *.mif* files from the zip.

    @param      filename    zip file
    @return                 dataframe
    """
    with zipfile.ZipFile(filename) as myzip:
        names0 = myzip.infolist()
        names = [_.filename for _ in names0 if _.filename.endswith(".mif")]
        if len(names) == 0:
            raise FileNotFoundError("No mif file in '{0}'".format(filename))
        with myzip.open(names[0], "r") as f:
            mif = f.read()
        names = [_.filename for _ in names0 if _.filename.endswith(".mid")]
        if len(names) == 0:
            raise FileNotFoundError("No mid file in '{0}'".format(filename))
        with myzip.open(names[0], "r") as f:
            mid = f.read()

    data = _read_geopandas_from_bytes(mif, mid)
    return data


def load_carreau_from_zip(file_car=None, file_rect=None):
    """
    Retourne un exemple de données carroyées.
    Les données sont disponibles dans le répertoire
    `data <https://github.com/sdpython/papierstat/tree/master/src/papierstat/datasets/data>`_.
    Notebooks associés à ce jeu de données :

    .. runpython::
        :rst:

        from papierstat.datasets.documentation import list_notebooks_rst_links
        links = list_notebooks_rst_links('visualisation', 'carte_carreau')
        links = ['    * %s' % s for s in links]
        print('\\n'.join(links))

    @param          file_car    les carreaux
    @param          file_rect   les données
    @return                     4 dataframes

    Résultats:

    * données sur la population par carreaux
    * shapefiles des carreaux
    * données sur la population par rectangles
    * shapefiles des rectangles

    .. note::

        Afin de respecter la règle de diffusion des données sur les
        revenus fiscaux des ménages, aucune information
        statistique (à l'exception du nombre total d'individus) n'est
        diffusée sur des carreaux de moins de 11 ménages. Ces carreaux de
        faibles effectifs sont donc regroupés en rectangles de taille plus
        importante et satisfaisant à cette règle des 11 ménages minimum.
        `source : INSEE <https://www.insee.fr/fr/statistiques/2520034>`_.
    """
    if file_rect is None and file_car is None:
        data = get_data_folder()
        file_rect = os.path.join(data, 'reunion_rect.zip')
        file_car = os.path.join(data, 'reunion.zip')
    dfcar = load_dbf_from_zip(file_car)
    shpcar = load_shapes_from_zip(file_car)
    dfrect = load_dbf_from_zip(file_rect)
    shprect = load_shapes_from_zip(file_rect)
    return dfcar, shpcar, dfrect, shprect
