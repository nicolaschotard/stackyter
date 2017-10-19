#!/usr/bin/env python

"""Setup script."""

import os
from setuptools import setup

# Long description loaded from the README
README = '/'.join(os.path.realpath(__file__).split('/')[:-1]) + '/README.rst'

# Get __version__ from version.py without importing package itself.
VERSION = '/'.join(os.path.realpath(__file__).split('/')[:-1]) + '/version.py'

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
      version=open(VERSION).read().split('"')[1],
      description=("Local display of a jupyter notebook running at CC-IN2P3"),
      license="MIT",
      classifiers=CLASSIFIERS,
      url="https://github.com/nicolaschotard/stackyter",
      author="Nicolas Chotard",
      author_email="nchotard@in2p3.fr",
      scripts=SCRIPTS,
      long_description=open(README).read(),
     )
