# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
import os
from setuptools import setup, Extension, find_packages
from pyquicksetup import read_version, read_readme, default_cmdclass


#########
# settings
#########

project_var_name = "papierstat"
versionPython = f"{sys.version_info.major}.{sys.version_info.minor}"
path = "Lib/site-packages/" + project_var_name
readme = 'README.rst'
history = "HISTORY.rst"
requirements = None

KEYWORDS = [project_var_name, 'Xavier Dupré', 'teachings', 'machine learning']
DESCRIPTION = """Helpers for teaching materials about machine learning."""
CLASSIFIERS = [
    'Programming Language :: Python :: 3',
    'Intended Audience :: Developers',
    'Topic :: Scientific/Engineering',
    'Topic :: Education',
    'License :: OSI Approved :: MIT License',
    'Development Status :: 5 - Production/Stable'
]

#######
# data
#######

packages = find_packages('src', exclude='src')
package_dir = {k: "src/" + k.replace(".", "/") for k in packages}
package_data = {project_var_name +
                ".datasets.data": ["*.csv", "*.txt", "*.zip", "*.gz", "*.json"]}

setup(
    name=project_var_name,
    version=read_version(__file__, project_var_name, subfolder='src'),
    author='Xavier Dupré',
    author_email='xavier.dupre@gmail.com',
    license="MIT",
    url=f"http://www.xavierdupre.fr/app/{project_var_name}/helpsphinx/index.html",
    download_url=f"https://github.com/sdpython/{project_var_name}/",
    description=DESCRIPTION,
    long_description=read_readme(__file__),
    cmdclass=default_cmdclass(),
    keywords=KEYWORDS,
    classifiers=CLASSIFIERS,
    packages=packages,
    package_dir=package_dir,
    package_data=package_data,
    # data_files=data_files,
    setup_requires=["pyquicksetup"],
    install_requires=['scikit-learn>=0.24.0', 'pandas>=1.0', 'mlinsights',
                      'matplotlib', 'pandas_streaming'],
    extras_require={
        'datasets.carreau': ["dbfread", "geopandas", "fiona"],
    },
)
