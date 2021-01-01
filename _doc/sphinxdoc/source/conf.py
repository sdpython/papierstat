# -*- coding: utf-8 -*-
import sys
import os
# import guzzle_sphinx_theme
import sphinx_bootstrap_theme
from pyquickhelper.helpgen.default_conf import set_sphinx_variables, get_default_stylesheet


sys.path.insert(0, os.path.abspath(os.path.join(os.path.split(__file__)[0])))

local_template = os.path.join(os.path.abspath(
    os.path.dirname(__file__)), "phdoc_templates")

set_sphinx_variables(__file__, "papierstat", "Xavier Dupré", 2021,
                     # "guzzle_sphinx_theme", guzzle_sphinx_theme.html_theme_path(),
                     "bootstrap", sphinx_bootstrap_theme.get_html_theme_path(),
                     locals(), extlinks=dict(
                         issue=('https://github.com/sdpython/papierstat/issues/%s', 'issue')),
                     title="papierstat", book=True, nblayout='table')

blog_root = "http://www.xavierdupre.fr/app/papierstat/helpsphinx/"
# extensions.append('guzzle_sphinx_theme')

if False:
    html_sidebars['**'] = ['globaltoc.html', 'localtoc.html', 'relations.html',
                           'sourcelink.html', 'searchbox.html']
    html_sidebars['*'] = html_sidebars['**']
    html_sidebars[''] = html_sidebars['*']

if html_theme == "bootstrap":
    html_theme_options = {
        'navbar_title': "BASE",
        'navbar_site_name': "Site",
        'navbar_links': [
            ("XD", "http://www.xavierdupre.fr", True),
        ],
        'navbar_sidebarrel': True,
        'navbar_pagenav': True,
        'navbar_pagenav_name': "Page",
        'bootswatch_theme': "readable",
        # united = weird colors, sandstone=green, simplex=red, paper=trop bleu
        # lumen: OK
        # to try, yeti, flatly, paper
        'bootstrap_version': "3",
        'source_link_position': "footer",
    }

html_context = {
    'css_files': get_default_stylesheet() + ['_static/my-styles.css', '_static/gallery.css'],
}


html_logo = "phdoc_static/project_ico.png"

language = "fr"

preamble = '''
\\usepackage{etex}
\\usepackage{fixltx2e} % LaTeX patches, \\textsubscript
\\usepackage{cmap} % fix search and cut-and-paste in Acrobat
\\usepackage[raccourcis]{fast-diagram}
\\usepackage{titlesec}
\\usepackage{amsmath}
\\usepackage{amssymb}
\\usepackage{amsfonts}
\\usepackage{graphics}
\\usepackage{epic}
\\usepackage{eepic}
%\\usepackage{pict2e}
%%% Redefined titleformat
\\setlength{\\parindent}{0cm}
\\setlength{\\parskip}{1ex plus 0.5ex minus 0.2ex}
\\newcommand{\\hsp}{\\hspace{20pt}}
\\newcommand{\\acc}[1]{\\left\\{#1\\right\\}}
\\newcommand{\\cro}[1]{\\left[#1\\right]}
\\newcommand{\\pa}[1]{\\left(#1\\right)}
\\newcommand{\\R}{\\mathbb{R}}
\\newcommand{\\HRule}{\\rule{\\linewidth}{0.5mm}}
%\\titleformat{\\chapter}[hang]{\\Huge\\bfseries\\sffamily}{\\thechapter\\hsp}{0pt}{\\Huge\\bfseries\\sffamily}
'''

custom_preamble = """\n
\\usepackage[all]{xy}
\\newcommand{\\vecteur}[2]{\\pa{#1,\\dots,#2}}
\\newcommand{\\N}[0]{\\mathbb{N}}
\\newcommand{\\indicatrice}[1]{\\mathbf{1\\!\\!1}_{\\acc{#1}}}
\\newcommand{\\infegal}[0]{\\leqslant}
\\newcommand{\\supegal}[0]{\\geqslant}
\\newcommand{\\ensemble}[2]{\\acc{#1,\\dots,#2}}
\\newcommand{\\fleche}[1]{\\overrightarrow{ #1 }}
\\newcommand{\\intervalle}[2]{\\left\\{#1,\\cdots,#2\\right\\}}
\\newcommand{\\loinormale}[2]{{\\cal N}\\pa{#1,#2}}
\\newcommand{\\independant}[0]{\\;\\makebox[3ex]{\\makebox[0ex]{\\rule[-0.2ex]{3ex}{.1ex}}\\!\\!\\makebox[.5ex][l]{\\rule[-.1ex]{.1ex}{2ex}}\\makebox[.5ex][l]{\\rule[-.1ex]{.1ex}{2ex}}} \\,\\,}
\\newcommand{\\esp}{\\mathbb{E}}
\\newcommand{\\var}{\\mathbb{V}}
\\newcommand{\\pr}[1]{\\mathbb{P}\\pa{#1}}
\\newcommand{\\loi}[0]{{\\cal L}}
\\newcommand{\\vecteurno}[2]{#1,\\dots,#2}
\\newcommand{\\norm}[1]{\\left\\Vert#1\\right\\Vert}
\\newcommand{\\norme}[1]{\\left\\Vert#1\\right\\Vert}
\\newcommand{\\dans}[0]{\\rightarrow}
\\newcommand{\\partialfrac}[2]{\\frac{\\partial #1}{\\partial #2}}
\\newcommand{\\partialdfrac}[2]{\\dfrac{\\partial #1}{\\partial #2}}
\\newcommand{\\loimultinomiale}[1]{{\\cal M}\\pa{#1}}
\\newcommand{\\trace}[1]{tr\\pa{#1}}
\\newcommand{\\sac}[0]{|}
\\newcommand{\\abs}[1]{\\left|#1\\right|}
"""
# \\usepackage{eepic}

imgmath_latex_preamble = preamble + custom_preamble
latex_elements['preamble'] = preamble + custom_preamble
mathdef_link_only = True

epkg_dictionary.update({
    'ACP': 'https://fr.wikipedia.org/wiki/Analyse_en_composantes_principales',
    'arbre de décision': 'https://fr.wikipedia.org/wiki/Arbre_de_d%C3%A9cision',
    'AUC': 'https://fr.wikipedia.org/wiki/Courbe_ROC',
    'C': "https://fr.wikipedia.org/wiki/C_(langage)",
    'csr_matrix': "https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.csr_matrix.html",
    'C++': "https://fr.wikipedia.org/wiki/C%2B%2B",
    'Enedis': "https://data.enedis.fr/page/accueil/",
    'ensae_teaching_cs': "http://www.xavierdupre.fr/app/ensae_teaching_cs/helpsphinx3/index.html",
    'ENSAE': "http://www.ensae.fr/ensae/fr/",
    'fiona': 'https://github.com/Toblerity/Fiona',
    'forêt aléatoire': 'https://fr.wikipedia.org/wiki/For%C3%AAt_d%27arbres_d%C3%A9cisionnels',
    'fortran': "https://fr.wikipedia.org/wiki/Fortran",
    'GeoDataFrame': 'http://geopandas.org/reference/geopandas.GeoDataFrame.html',
    'GeoJSON': 'https://fr.wikipedia.org/wiki/GeoJSON',
    'geopandas': 'http://geopandas.org/',
    'k-means': "http://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html",
    'machine learning': 'https://fr.wikipedia.org/wiki/Apprentissage_automatique',
    'Master 2 ISF': 'http://isf.u-paris2.fr/master-2/',
    'matrice de confusion': 'https://fr.wikipedia.org/wiki/Matrice_de_confusion',
    'mlstatpy': "http://www.xavierdupre.fr/app/mlstatpy/helpsphinx3/index.html",
    'OneHotEncoder': 'https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.OneHotEncoder.html',
    'Paris 2': 'https://www.u-paris2.fr/fr',
    'pickle': 'https://docs.python.org/3/library/pickle.html',
    'prophet': 'https://facebook.github.io/prophet/',
    'pyensae': 'http://www.xavierdupre.fr/app/pyensae/helpsphinx/',
    'R': "https://www.r-project.org/",
    'régression linéaire': 'https://fr.wikipedia.org/wiki/R%C3%A9gression_lin%C3%A9aire',
    'REST API': "https://en.wikipedia.org/wiki/Representational_state_transfer",
    'ROC': "http://www.xavierdupre.fr/app/mlstatpy/helpsphinx/c_metric/roc.html",
    'seaborn': "https://seaborn.pydata.org/",
    'statsmodels': "http://www.statsmodels.org/stable/index.html",
    'teachpyx': "http://www.xavierdupre.fr/app/teachpyx/helpsphinx3/index.html",
    'UCI': "http://archive.ics.uci.edu/ml/index.php",
})
