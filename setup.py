#!/usr/bin/env python

"""Setup script."""

from os import path
from setuptools import setup

here = path.abspath(path.dirname(__file__))

# Long description loaded from the README
with open(path.join(here, "README.rst")) as readme:
    long_description = readme.read()

# Get __version__ from version.py without importing package itself.    
with open(path.join(here, "version.py")) as version:
    version_number = version.read().split('"')[1]

# Package name
NAME = 'stackyter'

# Scripts (in scripts/)
SCRIPTS = ["stackyter.py"]

CLASSIFIERS = ['Development Status :: 3 - Alpha',
               'Intended Audience :: Science/Research',
               'Topic :: Software Development :: Build Tools',
               'License :: OSI Approved :: MIT License',
               'Programming Language :: Python :: 3',
               'Topic :: Scientific/Engineering :: Astronomy']

setup(name=NAME,
      version=version_number,
      description=("Local display of a jupyter notebook running at CC-IN2P3"),
      license="MIT",
      classifiers=CLASSIFIERS,
      url="https://github.com/nicolaschotard/stackyter",
      author="Nicolas Chotard",
      author_email="nchotard@in2p3.fr",
      scripts=SCRIPTS,
      long_description=long_description
     )
