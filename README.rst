stackyter
=========

LSST stack + Jupyter = stackyter

Available options and usage
===========================

  usage: stackyter.py [options]

  Run Jupyter on CC-IN2P3, setup the LSST stack, and display it localy.

  optional arguments:
  -h, --help           show this help message and exit
  --config CONFIG      Configuration file containing a set of option values.
                       The content of this file will be overwritten by any
        	       given command line option values shown below. (default:
	               None)
  --username USERNAME  Your CC-IN2P3 user name. Mandatory either from command
                       line or in the configuration file. (default: None)
  --workdir WORKDIR    Your working directory at CC-IN2P3 (default: \$HOME)
  --vstack VSTACK      Version of the stack you want to setup up. (default:
                       w_2017_38)
  --packages PACKAGES  A list of packages you want to setup. Coma separated
                       from command line, or a list in the config file.
                       (default: None)
  --jupyter JUPYTER    Either launch a jupiter notebook or a jupyter lab.
                       (default: notebook)
  --cca CCA            Either connecte to ccage or cca7. ccage might be used
                       for old version of the stack, whereas all newer version
                       (>v13) must be set up on centos7 (cca7). (default:
                       cca7)
