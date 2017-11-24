stackyter
=========

.. image:: https://landscape.io/github/nicolaschotard/stackyter/master/landscape.svg?style=flat
   :target: https://landscape.io/github/nicolaschotard/stackyter/master
   :alt: Code Health
	 
.. image:: https://badge.fury.io/py/stackyter.svg
    :target: https://badge.fury.io/py/stackyter

	   
Introduction
------------

This script will allow you to run a jupyter notebook (or lab) on a
distant server (default is CC-IN2P3) while displaying it localy in
your local brower. It was initialy intended to help LSST members to
interact with the datasets already available at CC-IN2P3 using Python
(in a ``stack`` or a DESC environment), but can be use for other
purposes that need a Jupyter environment. It can be used in the
following mode:

- For LSST/DESC members:

  - LSST stack environment using the ``--vstack`` option.
  - DESC catalogs environment using the ``--desc`` option
  - Your personal setup using the ``--mysetup`` option

- For all users:

  - With your personal setup using the ``--mysetup`` option
  - On any host (not only CC-IN2P3) using the ``--host`` **AND** the
    ``--mysetup`` options together.

   
**Jupyter must be available on the distant host for this script to work.**

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

By default, ``stackyter`` will try to connect to CC-IN2P3 using what
``ssh`` can find in your ``~/.ssh/config`` or taking your local user
name. It will also set up the latest stable version of the LSST
stack. If this is not what you want to do, use the following set of
options to adapt ``stackyter`` to your personal case.

Options and configurations
--------------------------

Optional arguments
~~~~~~~~~~~~~~~~~~

An option used on the command line will always overwrite the content
of the configuration file for the same option, if it exists. See the
next section for a description on how to use the configuration
file. Available options are::

  -h, --help           show this help message and exit
  --config CONFIG      Configuration file containing a set of option values.
                       The content of this file will be overwritten by any
                       given command line options. You can also give the name
                       of a configuration if you have defined it in your
                       default configuration file. See the documentation for
                       details on how to build this file. (default: None)
  --username USERNAME  Your CC-IN2P3 user name. If not given, ssh will try to
                       figure it out from you ~/.ssh/config or will use your
                       local user name. (default: None)
  --host HOST          Name of the target host. This option may allow you to
                       avoid potential conflit with the definition of the same
                       host in your $HOME/.ssh/config, or to connect to an
                       other host than the CC-IN2P3 ones (Jupyter must also be
                       available on these hosts). Default if to connect to CC-
                       IN2P3. (default: cca7.in2p3.fr)
  --workdir WORKDIR    Your working directory at CC-IN2P3 (default:
                       /pbs/throng/lsst/users/<username>/notebooks)
  --jupyter JUPYTER    Either launch a jupiter notebook or a jupyter lab.
                       (default: notebook)
  --vstack VSTACK      Version of the stack you want to set up. (E.g. v14.0,
                       w_2017_43 or w_2017_43_py2) (default: v14.0)
  --packages PACKAGES  A list of packages you want to setup. Coma separated
                       from command line, or a list in the config file. You
                       can use the `lsst_distrib` package to set up all
                       available packages from a given distrib. (default:
                       lsst_distrib)
  --desc               Setup a DESC environment giving you access to DESC
                       catalogs ('proto-dc2_v2.0' is for now the only
                       available catalog). This option overwrites the '--
                       vstack' and '--mysetup' options. (default: False)
  --mysetup MYSETUP    Path to a setup file (at CC-IN2P3) that will be used to
                       set up the working environment. Be sure that a Python
                       installation with Jupyter (and jupyterlab) is available
                       to make this work. The LSST stack won't be set up in
                       this mode. 'vstack', 'libs', 'bins' and 'labpath'
                       options will be ignored. (default: None)
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


Configuration file
~~~~~~~~~~~~~~~~~~

A configuration dictionnary can contain any options available through
the command line. The options found in the configuration file will
always be overwritten by the command line.

The configuration file can be given in different ways, and can
contains from a single configuration dictionnary to several
configuration dictionnaries. The ``--config`` and ``--congfile``
options can be used (or not) in several different ways:

- ``stackyter.py --configfile myfile.yaml``. ``myfile.yaml`` must contain
  your configuration, with your set of options.

- ``stackyter.py --config myconfig``. In that case, no configuration
  is directly given by the user, and ``stakyter`` will look for a
  default configuration file. The default file must be either
  ``~/stackyter-config.yaml`` or defined by the ``STACKYTERCONFIG``
  environment variable, that you must have previoulsy define in case
  the default value does not fit your need. The ``myconfig`` key will
  then be looked for in this default configuration file to get the
  configuration dictionnart that you asked for.

- ``stackyter.py``. In that case, ``stackyter`` will also look for a
  default configuration file (see above), and for a default
  configuration called ``default_config`` in this file. Thi sdefault
  must point to the configuration you would like to use by
  default.

In principal, your default configuration file must look like that::

  {
   'default_config': 'ccin2p3',
   'ccin2p3': {
               'host': 'cca7.in2p3.fr',  # or ccjupyter if your ~/.ssh/config if configured
               'jupyter': 'lab',
               'packages': ["lsst_distrib"],
               'username': 'nchotard',
               'vstack': 'v14.0',
               'workdir': '/sps/lsst/dev/nchotard/',
              },
   'othersite': {
                 'host': 'otherhost.fr',
                 'username': 'chotard',
                 'mysetup': 'pathtomysetup'
                },
  }

or simply as followed if only one configuration is defined::

  {
   'ccin2p3': {
               'host': 'cca7.in2p3.fr',  # or ccjupyter if your ~/.ssh/config if configured
               'jupyter': 'lab',
               'packages': ["lsst_distrib"],
               'username': 'nchotard',
               'vstack': 'v14.0',
               'workdir': '/sps/lsst/dev/nchotard/',
              },
  }



Distant host configuration
--------------------------

The ``--host`` option allows you to connect to any distant host. The
default option used to create the ``ssh`` tunnel are ``-X -Y -tt
-L``. If you want to configure your ``ssh`` connection, edit your
``~/.ssh/config`` file using, for instance, the following template::

  Host ccjupyter
  Hostname cca7.in2p3.fr
  User lsstuser
  GSSAPIClientIdentity lsstuser@IN2P3.FR
  GSSAPIAuthentication yes
  GSSAPIDelegateCredentials yes
  GSSAPITrustDns yes

You can then use the ``stackyter`` script as follows::

  stackyter.py --host ccjupyter

Or put the value for that option (along with others) in your
``config.yaml`` file. Do not forget to change ``lsstuser`` by your
personal user name.

LSST environment
----------------
		  
Version of the LSST stack
~~~~~~~~~~~~~~~~~~~~~~~~~

All available versions of the LSST stack at CC-IN2P3 can be found under::

  /sps/lsst/software/lsst_distrib/

These versions (and all the others) have been built under CentOS7, and
must be used under a compatible system (CentOS7 or Ubuntu). To connect
to a CentOS7 machine on CC-IN2P3, use ``--host cca7.in2p3.fr`` instead
of ``--host ccage.in2p3.fr`` (``cca7`` is the default value of this
script).

Python 2 (2.7) and 3 (>3.4) are available for almost all weeklies,
with the following nomencalture:

+----------+-------------------+-------------------+
| Version  | < ``w_2017_27``   | ``w_2017_27``     |
+==========+===================+===================+
| Python 2 | ``w_2017_XX``     | ``w_2017_XX_py2`` |
+----------+-------------------+-------------------+
| Python 3 | ``w_2017_XX_py3`` | ``w_2017_XX``     |
+----------+-------------------+-------------------+

Latest releases of the LSST stack, as of 11-07-2017, are:

+-------------------+-----------------------------------------------------+
| Version           | Comment                                             |
+===================+=====================================================+
| ``v14.0``         | Current stable version of the stack (Python 3 only) |
+-------------------+-----------------------------------------------------+
| ``w_2017_43_py2`` | Latest weekly release for Python 2                  |
+-------------------+-----------------------------------------------------+
| ``w_2017_44``     | Latest weekly release for Python 3                  |
+-------------------+-----------------------------------------------------+

Keep in mind that using Python 2 in an LSST context is not encouraged
by the community, and will not be supported anymore. The latest weekly
for which Python 2 has been installed at CC-IN2P3 is ``w_2017_4`` (see
online `documentation
<http://doc.lsst.eu/ccin2p3/ccin2p3.html#software>`_).

**Note**: Since version ``w_2017_40``, the ``ipython`` module is
included in the stack installation at CC-IN2P3 as an add-on. This
module is not part of the officiel LSST distribution and will not be
set up with the ``lsst_distrib`` package.

Use the LSST stack
~~~~~~~~~~~~~~~~~~

Many examples on how to use the LSST stack and how to work with its
outputs are presented `there
<https://github.com/nicolaschotard/lsst_drp_analysis/tree/master/stack>`_.

A few data sets have already been re-processed using the LSST stack,
and their outputs are available for analysis at different places on
CC-IN2P3:

- SXDS data from HSC: ``/sps/lsst/dev/lsstprod/hsc/SXDS/output``
- CFHT data (containing clusters): ``/sps/lsst/data/clusters``
- CFHT D3 fieald: ``/sps/lsst/data/CFHT/D3``

Additional features
~~~~~~~~~~~~~~~~~~~

- ``ds9`` is automatically available since version 0.9, and can be
  called in a Jupyter terminal.

DESC environment
----------------

You can automatically set up an ``anaconda`` working environment that
will give you access to DESC catalogs such as the lattest
``proto-dc2_v2.0``::

  stackyter.py --desc

A test notebook is available on `this github page
<https://github.com/LSSTDESC/gcr-catalogs/blob/master/examples/GCRCatalogs%20Demo.ipynb>`_. Download
it and run it to make sure that everything is working properly. In
this environment, the following ressources are available:

- A ``miniconda3`` install with ``Jupyter`` (notebook and lab) and ``Ipython``;
- The `GRC <https://github.com/yymao/generic-catalog-reader>`_
  (Generic Catalog Reader) and `grc-catalogs
  <https://github.com/LSSTDESC/gcr-catalogs>`_ packages, allowing you
  to easily load and read the DESC catalogs;
- The following DESC catalogs (more info can be found on the `grc-catalogs
  <https://github.com/LSSTDESC/gcr-catalogs>`_ web page):

  - ``proto-dc2_v2.0``

- You can also use the ``--libs`` or ``--bins`` options to complete this
  set up with your personnal libraries (Python 3 only for now).
  
Personal environment
--------------------

As stated in the introduction, and instead of seting up the LSST/DESC
working environments, you can set up your personal working environment
by using the ``--mysetup`` option. Given a setup file located an your
distant host, you can simply do::

  stackyter.py --mysetup /path/to/my/setup.sh (--username myusername)

Your local setup file will be sourced at connection as followed::

  source /path/to/my/setup.sh

Your setup file must **at least** contains what is needed to make
Jupyter available. In this mode, the LSST stack will **not** be setup.

You can also use the ``--host`` option to run on an different distant
host than CC-IN2P3.

Questions?
----------

- If you have any comments or suggestions, or if you find a bug,
  please use the dedicated github `issue tracker
  <https://github.com/nicolaschotard/stackyter/issues>`_ for this
  page.
- Why ``stakyter``? For historical reason: ``stackyter`` = LSST ``stack`` +
  ``Jupyter``. It was initially intended for LSST members to easily use the
  LSST software stack and interact with the data sets.
