stackyter
=========

LSST stack + Jupyter = stackyter

This script will allow you to run a jupyter notebook (or lab) at
CC-IN2P3 while displaying it localy in your local brower. It is mainly
intended to help LSST members to interact with the datasets already
available at CC-IN2P3 using Python. But setting up the LSST stack is
not mandatory, making this script useful in other (LSST) contexts
where a Jupyter notebook is needed.

Usage
-----

::
   
   stackyter.py [options]

The configuration file can contain any (or all) options available
through command line. An example of such a file can be found `here
<example_config.yaml>`_. The only option that you **must** use is the
`--username` option.


Options
-------

::

  optional arguments:
  -h, --help           show this help message and exit
  --config CONFIG      Configuration file containing a set of option values.
                       The content of this file will be overwritten by any
                       given command line options. (default: None)
  --username USERNAME  Your CC-IN2P3 user name. Mandatory either from command
                       line or in the configuration file. (default: None)
  --workdir WORKDIR    Your working directory at CC-IN2P3 (default: \$HOME)
  --vstack VSTACK      Version of the stack you want to setup up. If not
                       given, the LSST stack will not be set up. (E.g. v13.0,
                       w_2017_42 or w_2017_42_py2) (default: None)
  --packages PACKAGES  A list of packages you want to setup. Coma separated
                       from command line, or a list in the config file.
                       (default: None)
  --jupyter JUPYTER    Either launch a jupiter notebook or a jupyter lab.
                       (default: notebook)
  --cca CCA            Either connect to ccage or cca7. ccage might be used
                       for old or local install of the stack, whereas all
                       newer versions (> v13.0, installed for the LSST group)
                       must be set up on centos7 (cca7). (default: cca7)
  --libs LIBS          Path(s) to local Python librairies (must contains the
                       lib and bin directories). Will be added to your PATH
                       and PYTHONPATH. Coma separated to add more than one
                       paths, or a list in the config file. A default path for
                       jupyter will be choose if not given. (default: None)
  --labpath LABPATH    You must provide the path in which jupyterlab has been
                       installed in case it differs from the (first) path you
                       gave to the --libs option. A default path for
                       jupyterlab will be choose if not given. (default: None)


Version of the LSST stack
-------------------------

All available versions of the LSST stack at CC-IN2P3 can be found under::

  /sps/lsst/software/lsst_distrib/

A few of them that you might want to use are::

  v13.0  -> stable version of the stack 13
  w_2017_42  -> latest (as of 10-23-2017) weekly release, python 3
  w_2017_42_py2  -> latest weekly release, python 2

These versions (and all the others) have been built under CentOS7, and
must be used under a compatible system (CentOS7 or Ubuntu). To connect
to a CentOS7 machine on CC-IN2P3, use cca7 instead of ccage (default
value of this script).

Version 2 (2.7) and 3 (>3.4) are available for almost all weeklies, with following nomencalture:

- for weeklies < `w_2017_27`:
  - Python 2 -> `w_2017_??`
  - Python 3 -> `w_2017_??_py3`
- for weeklies >= `w_2017_27`:
  - Python 2 -> `w_2017_??_py2`
  - Python 3 -> `w_2017_??`

Use the LSST stack
------------------

Many examples on how to use the LSST stack and how to work with its
outputs are presented `here
<https://github.com/nicolaschotard/lsst_drp_analysis/tree/master/stack>`_.

A few data sets have already been created using the LSST stack, and
their outputs are already available for analaysis at different places
on CC-IN2P3:

- SXDS data from HSC: `/sps/lsst/dev/lsstprod/hsc/SXDS/output`
- CFHT data (containing clusters): `/sps/lsst/data/clusters`
- list to be completed.
