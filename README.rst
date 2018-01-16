.. image:: http://readthedocs.org/projects/stackyter/badge/?version=latest
   :target: http://stackyter.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. image:: https://landscape.io/github/nicolaschotard/stackyter/master/landscape.svg?style=flat
   :target: https://landscape.io/github/nicolaschotard/stackyter/master
   :alt: Code Health
	 
.. image:: https://badge.fury.io/py/stackyter.svg
    :target: https://badge.fury.io/py/stackyter

.. inclusion-marker-do-not-remove	

stackyter
=========

This script allow you to run a jupyter notebook (or lab) on a
distant server (default is CC-IN2P3) while displaying it localy in
your local brower. It was initialy intended to help LSST members to
interact with the datasets already available at CC-IN2P3 using Python
(in a ``stack`` or a DESC environment), but can be use for other
purposes that need a Jupyter environment. It can be used in the
following mode:

- For all users:

  - On any host using the ``--host`` option.
  - With your personal setup using the ``--mysetup`` option.

- For LSST/DESC members (at CC-IN2P3):

  - Your personal setup using the ``--mysetup`` option (as above).
  - LSST stack environment using the ``--vstack`` option.
  - DESC catalogs environment using the ``--desc`` option.

   
**Jupyter must be available on the distant host for this script to work.**

Installation
============

Latest stable version can be installed with ``pip``::

  pip install stackyter
   
To upgrade to a newer version::

  pip install --upgrade stackyter

To install in a local directory::

   pip install --user stackyter            #  in your home directory
   pip install --prefix mypath stackyter   #  in 'mypath'


Usage
=====

.. code-block:: shell
   
   stackyter.py [options]


Then click on the green link given by ``stackyter``, as followed::
  
    Copy/paste this URL into your browser to run the notebook localy 
       http://localhost:20001/?token=38924c48136091ade71a597218f2722dc49c669d1430db41



``Ctrl-C`` will stop the Jupyter server and close the connection.

By default, ``stackyter`` will try to connect to CC-IN2P3 using what
``ssh`` can find in your ``~/.ssh/config`` or taking your local user
name. It will also set up the latest stable version of the LSST
stack. If this is not what you want to do, use the following set of
options to adapt ``stackyter`` to your personal case.

Options and configurations
==========================

Optional arguments
------------------

An option used on the command line will always overwrite the content
of the configuration file for the same option, if it exists. See the
next section for a description on how to use the configuration
file. Available options are::

  General:
    General options for any host on which Jupyter can be found
  
    -c CONFIG, --config CONFIG
                          Name of the configuration to use, taken from your
                          default configuration file (~/.stackyter-config.yaml
                          or $STACKYTERCONFIG). Default if to use the
                          'default_config' defined in this file. The content of
                          the configuration file will be overwritten by any
                          given command line options. (default: None)
    -f CONFIGFILE, --configfile CONFIGFILE
                          Configuration file containing a set of option values.
                          The content of this file will be overwritten by any
                          given command line options. (default: None)
    -H HOST, --host HOST  Name of the target host. Allows you to avoid conflit
                          with the content of your $HOME/.ssh/config, or to
                          connect to any host on which Jupyter is available.
                          (default: cca7.in2p3.fr)
    -u USERNAME, --username USERNAME
                          Your user name on the host. If not given, ssh will try
                          to figure it out from you ~/.ssh/config or will use
                          your local user name. (default: None)
    -w WORKDIR, --workdir WORKDIR
                          Your working directory on the host (default: None)
    --mysetup MYSETUP     Path to a setup file (on the host) that will be used
                          to set up the working environment. A Python
                          installation with Jupyter must be available to make
                          this work. (default: None)
    -j JUPYTER, --jupyter JUPYTER
                          Either launch a jupiter notebook or a jupyter lab.
                          (default: notebook)
    --libs LIBS           Path(s) to local Python librairies. Will be added to
                          your PYTHONPATH. Coma separated to add more than one
                          paths, or a list in the config file. (default: None)
    --bins BINS           Path(s) to local binaries. Will be added to your PATH.
                          Coma separated to add more than one paths, or a list
                          in the config file. (default: None)
    --labpath LABPATH     Path in which jupyterlab has been installed in case it
                          differs from the (first) path you gave to the --libs
                          option. (default: None)
    -C, --compression     Activate ssh compression option (-C). (default: False)
    -S, --showconfig      Show all available configurations from your default
                          file and exit. (default: False)
  
  LSST/DESC at CC-IN2P3:
    Shortcuts to access the LSST stack or the DESC catalogs at CC-IN2P3
  
    --vstack VSTACK       Version of the stack you want to set up. (E.g. v14.0,
                          w_2017_43 or w_2017_43_py2) (default: v14.0)
    --packages PACKAGES   A list of packages you want to setup. Coma separated
                          from command line, or a list in the config file.
                          `lsst_distrib` will set up all available packages.
                          (default: lsst_distrib)
    --desc                Setup a DESC environment giving you access to DESC
                          catalogs. Overwrites the '--mysetup' and '--vstack'
                          options. (default: False)


Configuration file
------------------

A configuration dictionnary can contain any options available through
the command line. The options found in the configuration file will
always be overwritten by the command line.

The configuration file can be given in different ways, and can
contains from a single configuration dictionnary to several
configuration dictionnaries:

- The **configuration file** can either be a default file located
  under ``~/stackyter-config.yaml`` or defined by the
  ``STACKYTERCONFIG``, or given in command line using the
  ``--configfile`` option.

- The **configuration name**, which should be defined in your
  configuration file, must be given using the command line option
  ``--config``. If not given, a ``default_config``, which should be
  defined in your configration file, will be used by default.

Here are a few example on how to use it::

  stackyter.py  # 'default_config' in default file if it exists, default option values used otherwise
  stackyter.py --config config1  # 'config1' in default file which must exist
  stackyter.py --config config2 --configfile myfile.yaml  # 'config2' in 'myfile.yaml'
  stackyter.py --configfile myfile.yaml  # 'default_config' in 'myfile.yaml'

In principal, your default configuration file should look like that::

  {
   'default_config': 'host1',
  
   'host1': {
             'host': 'myhost.domain.fr',  # or 'myhost' if you have configured your ~/.ssh/config file
             'jupyter': 'lab',  # if installed
             'username': 'myusername',
             'mysetup': '/path/to/my/setup/file.sh',
             'workdir': '/path/to/my/directory/'
              },
  
   'host2': {
             'host': 'otherhost.fr',
             'username': 'otherusername',
             'mysetup': '/path/to/my/setup'
            },
  
   'stack': {
             'host': 'cca7.in2p3.fr',  # or ccjupyter if you have configured your ~/.ssh/config file
             'packages': ["lsst_distrib"],
             'username': 'myusername',
             'vstack': 'v14.0',
             'workdir': '/pbs/throng/lsst/users/username/',
              },
  
   'desc': {
            'host': 'cca7.in2p3.fr',
            'username': 'myusername',
            'desc': True,
            'workdir': '/pbs/throng/lsst/users/username/'
           }
  }

or simply as followed if only one configuration is defined::

  {
   'host1': {
             'host': 'myhost.domain.fr',  # or 'myhost' if you have configured your ~/.ssh/config file
             'jupyter': 'lab',  # if installed
             'username': 'myusername',
             'mysetup': '/path/to/my/setup/file.sh',
             'workdir': '/path/to/my/directory/'
              },
  }

You can use the `example
<https://raw.githubusercontent.com/nicolaschotard/stackyter/master/example-config.yaml>`_
configuration file as a template to create your own.


Distant host configuration
==========================

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

Personal environment
====================

As stated in the introduction, you can set up your personal working
environment by using the ``--mysetup`` option. Given a setup file
located an your distant host, you can simply do::

  stackyter.py --mysetup /path/to/my/setup.sh (--username myusername)

Your local setup file will be sourced at connection as followed::

  source /path/to/my/setup.sh

Your setup file must **at least** contains what is needed to make
Jupyter available. In this mode, the LSST stack will **not** be setup.

You can also use the ``--host`` option to run on an different distant
host than CC-IN2P3.

LSST environment
================
		  
Version of the LSST stack
-------------------------

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

Latest releases of the LSST stack, as of 12-12-2017, are:

+-------------------+-----------------------------------------------------+
| Version           | Comment                                             |
+===================+=====================================================+
| ``v14.0``         | Current stable version of the stack (Python 3 only) |
+-------------------+-----------------------------------------------------+
| ``w_2017_43_py2`` | Latest weekly release for Python 2                  |
+-------------------+-----------------------------------------------------+
| ``w_2017_52``     | Latest weekly release for Python 3                  |
+-------------------+-----------------------------------------------------+

Keep in mind that using Python 2 in an LSST context is not encouraged
by the community, and will not be supported anymore. The latest weekly
for which Python 2 has been installed at CC-IN2P3 is ``w_2017_43`` (see
online `documentation
<http://doc.lsst.eu/ccin2p3/ccin2p3.html#software>`_).

**Note**: Since version ``w_2017_40``, the ``ipython`` module is
included in the stack installation at CC-IN2P3 as an add-on. This
module is not part of the officiel LSST distribution and will not be
set up with the ``lsst_distrib`` package.

Use the LSST stack
------------------

Many examples on how to use the LSST stack and how to work with its
outputs are presented `there
<https://github.com/nicolaschotard/lsst_drp_analysis/tree/master/stack>`_.

A few data sets have already been re-processed using the LSST stack,
and their outputs are available for analysis at different places on
CC-IN2P3:

- SXDS data from HSC: ``/sps/lsst/users/lsstprod/hsc/SXDS/output``
- CFHT data (containing clusters): ``/sps/lsst/data/clusters``
- CFHT D3 fieald: ``/sps/lsst/data/CFHT/D3``

Additional features
-------------------

- ``ds9`` is automatically available since version 0.9, and can be
  called in a Jupyter terminal.

DESC environment
================

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

Help
====

- If you have any comments or suggestions, or if you find a bug,
  please use the dedicated github `issue tracker
  <https://github.com/nicolaschotard/stackyter/issues>`_.
- Why ``stakyter``? For historical reason: ``stackyter`` = LSST
  ``stack`` + ``Jupyter``. It was initially intended for LSST members
  to easily use the LSST software stack and interact with data sets.
