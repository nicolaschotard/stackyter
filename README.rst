stackyter
=========

.. image:: https://landscape.io/github/nicolaschotard/stackyter/master/landscape.svg?style=flat
   :target: https://landscape.io/github/nicolaschotard/stackyter/master
   :alt: Code Health
	 
.. image:: https://badge.fury.io/py/stackyter.svg
    :target: https://badge.fury.io/py/stackyter

Introduction
------------

LSST stack + Jupyter -> stackyter

This script will allow you to run a jupyter notebook (or lab) at
CC-IN2P3 while displaying it localy in your local brower. It is mainly
intended to help LSST members to interact with the datasets already
available at CC-IN2P3 using Python.


Installation
------------

Latest stable version can be installed with ``pip``::

  pip install stackyter
   
To upgrade to a newer version::

  pip install --upgrade stackyter

To install in a local directory::

   pip install --user stackyter            #  in your home directory
   pip install --prefix mypath stackyter   #  in 'mypath'


Usage
-----

.. code-block:: shell
   
   stackyter.py [options]


Options
-------

The configuration file can contain any (or all) options available
through command line. An example of such a file can be found `here
<https://github.com/nicolaschotard/stackyter/blob/master/example_config.yaml>`_. The
only option that you **must** use is the ``--username`` option.

Optional arguments are::

  -h, --help           show this help message and exit
  --config CONFIG      Configuration file containing a set of option values.
                       The content of this file will be overwritten by any
                       given command line options. (default: None)
  --username USERNAME  Your CC-IN2P3 user name. Mandatory either from command
                       line or in the configuration file. (default: None)
  --workdir WORKDIR    Your working directory at CC-IN2P3 (default:
                       /pbs/throng/lsst/users/<username>/notebooks)
  --vstack VSTACK      Version of the stack you want to set up. (E.g. v14.0,
                       w_2017_42 or w_2017_42_py2) (default: v14.0)
  --packages PACKAGES  A list of packages you want to setup. Coma separated
                       from command line, or a list in the config file. You
                       can use the `lsst_distrib` package to set up all
                       available packages from a given distrib. (default:
                       lsst_distrib)
  --jupyter JUPYTER    Either launch a jupiter notebook or a jupyter lab.
                       (default: notebook)
  --cca CCA            Either connect to ccage or cca7. ccage might be used
                       for old or local install of the stack, whereas all
                       newer versions (>= v13.0, installed for the LSST group)
                       must be set up on centos7 (cca7). (default: cca7)
  --libs LIBS          Path(s) to local Python librairies. Will be added to
                       your PYTHONPATH. Coma separated to add more than one
                       paths, or a list in the config file. A default path for
                       jupyter will be choose if not given. (default: None)
  --bins BINS          Path(s) to local binaries. Will be added to your PATH.
                       Coma separated to add more than one paths, or a list in
                       the config file. A default path for jupyter will be
                       choose if not given. (default: None)
  --labpath LABPATH    You must provide the path in which jupyterlab has been
                       installed in case it differs from the (first) path you
                       gave to the --libs option. A default path for
                       jupyterlab will be choose if not given. (default: None)


Version of the LSST stack
-------------------------

All available versions of the LSST stack at CC-IN2P3 can be found under::

  /sps/lsst/software/lsst_distrib/

A few of them that you might want to use are::

  v14.0  -> current stable version of the stack (Python 3 only)
  w_2017_42  -> latest (as of 10-25-2017) weekly release, Python 3
  w_2017_42_py2  -> latest weekly release, Python 2

These versions (and all the others) have been built under CentOS7, and
must be used under a compatible system (CentOS7 or Ubuntu). To connect
to a CentOS7 machine on CC-IN2P3, use cca7 instead of ccage (default
value of this script).

Version 2 (2.7) and 3 (>3.4) are available for almost all weeklies,
with the following nomencalture:

- for weeklies < `w_2017_27`:
  
  - python 2 -> `w_2017_??`
  - python 3 -> ``w_2017_??_py3`
    
- for weeklies >= `w_2017_27`:
  
  - python 2 -> `w_2017_??_py2`
  - python 3 -> `w_2017_??`

Keep in mind that using Python 2 in an LSST context is not encouraged
by the community, and will not be supported anymore. The latest weekly
for which Python 2 will be installed at CC-IN2P3 will be `w_2017_44`
(see online documentation `here
<http://doc.lsst.eu/ccin2p3/ccin2p3.html#software>`_).

**Note**: Since version `w_2017_40`, the ``ipython`` module is
included in the stack installation at CC-IN2P3 as an add-on. This
module is not part of the officiel LSST distribution and will not be
set up with the ``lsst_distrib`` package.

Use the LSST stack
------------------

Many examples on how to use the LSST stack and how to work with its
outputs are presented `here
<https://github.com/nicolaschotard/lsst_drp_analysis/tree/master/stack>`_.

A few data sets have already been created using the LSST stack, and
their outputs are already available for analysis at different places
on CC-IN2P3:

- SXDS data from HSC: ``/sps/lsst/dev/lsstprod/hsc/SXDS/output``
- CFHT data (containing clusters): ``/sps/lsst/data/clusters``
- list to be completed.
