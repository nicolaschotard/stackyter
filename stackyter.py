#!/usr/bin/env python
"""Run jupyter on a given host and display it localy."""


import os
import sys
import subprocess
from argparse import ArgumentParser
from argparse import ArgumentDefaultsHelpFormatter
import yaml
import numpy as np


DEFAULT_CONFIG = os.getenv("HOME") + "/.stackyter-config.yaml"


def string_to_list(a):
    """Transform a string with coma separated values to a list of values."""
    return a if isinstance(a, list) or a is None else a.split(",")


def get_default_config(only_path=False):
    """Get the stackyter default configuration file if it exists."""
    if os.getenv("STACKYTERCONFIG") is not None:  # set up by the user
        config = os.getenv("STACKYTERCONFIG")
        if not os.path.exist(config):
            raise IOError("$STACKYTERCONFIG is defined but the file does not exist.")
    elif os.path.exists(DEFAULT_CONFIG):  # default location
        config = DEFAULT_CONFIG
    else:
        return None
    return yaml.load(open(config, 'r')) if not only_path else config


def read_config(config, key=None):
    """Read a config file and return the right configuration."""
    print("INFO: Loading configuration from", config)
    config = yaml.load(open(config, 'r'))
    if key is not None:
        if key in config:
            print("INFO: Using the '%s' configuration" % key)
            config = config[key]
        else:
            raise IOError("Configuration `%s` does not exist. Check your default file." % key)
    elif len(config) > 1:
        if 'default_config' in config:
            print("INFO: Using default configuration '%s'" % config['default_config'])
            config = config[config['default_config']]
        else:
            raise IOError("You must define a 'default_config' in you configuration file.")
    else:
        config = config[list(config)[0]]
    return config


def get_config(config, configfile):
    """Get the configuration for stackyter is any."""
    configfile = get_default_config(only_path=True) if configfile is None else configfile
    if config is not None:
        # Is there a configuration file?
        if configfile is None:
            raise IOError("No (default) configuration file found or given. Check the doc.")
        config = read_config(configfile, key=config)
    elif configfile is not None:
        config = read_config(configfile)
    return config


if __name__ == '__main__':

    description = """Run Jupyter on a given host and display it localy."""
    prog = "stackyter.py"
    usage = """%s [options]""" % prog

    parser = ArgumentParser(prog=prog, usage=usage, description=description,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    general = parser.add_argument_group('General', 'General options for any host on which '
                                        ' Jupyter can be found')

    # General options
    general.add_argument('-c', '--config', default=None,
                         help='Name of the configuration to use, taken from your default '
                         'configuration file (~/.stackyter-config.yaml or $STACKYTERCONFIG). '
                         "Default if to use the 'default_config' defined in this file. "
                         'The content of the configuration file will be overwritten by any '
                         'given command line options.')
    general.add_argument('-f', '--configfile', default=None,
                         help='Configuration file containing a set of option values. The content '
                         'of this file will be overwritten by any given command line options.')
    general.add_argument('-H', "--host", default="cca7.in2p3.fr",
                         help="Name of the target host. Allows you to avoid conflit with the "
                         "content of your $HOME/.ssh/config, or to connect to any host on which "
                         "Jupyter is available.")
    general.add_argument('-u', '--username',
                         help="Your user name on the host. If not given, ssh will try to "
                         "figure it out from you ~/.ssh/config or will use your local user name.")
    general.add_argument('-w', "--workdir", default=None,
                         help="Your working directory on the host")
    general.add_argument("--mysetup", default=None,
                         help="Path to a setup file (on the host) that will be used to set up the "
                         "working environment. A Python installation with Jupyter must be "
                         "available to make this work.")
    general.add_argument('-j', "--jupyter", default="notebook",
                         help="Either launch a jupiter notebook or a jupyter lab.")
    general.add_argument("--libs", default=None,
                         help="Path(s) to local Python librairies. Will be added to your PYTHONPATH."
                         " Coma separated to add more than one paths, or a list in the config file.")
    general.add_argument("--bins", default=None,
                         help="Path(s) to local binaries. Will be added to your PATH."
                         " Coma separated to add more than one paths, or a list in the config file.")
    general.add_argument("--labpath", default=None,
                         help="Path in which jupyterlab has been installed in case it differs from "
                         "the (first) path you gave to the --libs option.")
    general.add_argument('-C', '--nocompression', action='store_true', default=False,
                         help='Deactivate ssh compression options.')
    general.add_argument('-S', '--showconfig', action='store_true', default=False,
                         help='Show all available configurations from your default file and exit.')

    # LSST/DESC @ CC-IN2P3 options
    lsstdesc = parser.add_argument_group('LSST/DESC at CC-IN2P3', 'Shortcuts to access the LSST '
                                         'stack or the DESC catalogs at CC-IN2P3')
    lsstdesc.add_argument("--vstack", default='v14.0',
                          help="Version of the stack you want to set up."
                          " (E.g. v14.0, w_2017_43 or w_2017_43_py2)")
    lsstdesc.add_argument("--packages", default='lsst_distrib',
                          help="A list of packages you want to setup. Coma separated from command"
                          " line, or a list in the config file. `lsst_distrib` will set up all "
                          "available packages.")
    lsstdesc.add_argument("--desc", action='store_true', default=False,
                          help="Setup a DESC environment giving you access to DESC catalogs. "
                          "Overwrites the '--mysetup' and '--vstack' options.")

    args = parser.parse_args()

    # Show available configuration(s) is any and exit
    if args.showconfig:
        config = get_default_config(only_path=True)
        if config is not None:
            config = open(config, 'r')
            print("Your default configuration file contains the following configuration(s).")
            print(config.read())
            config.close()
        else:
            print("Error: No default configuration file found.")
        sys.exit(0)

    # Do we have a configuration file
    config = get_config(args.config, args.configfile)
    if config is not None:
        for opt, val in args._get_kwargs():
            # only keep option value from the config file
            # if the user has not set it up from command line
            if opt in config and '--' + opt not in sys.argv:
                setattr(args, opt, config[opt])

    # A valid username (and the corresponding password) is actually the only mandatory thing we need
    args.username = "" if args.username is None else args.username + "@"

    # Make sure that we have a list (even empty) for packages
    args.packages = string_to_list(args.packages)

    # A random port number is selected between 1025 and 65635 (included) for server side to
    # prevent from conflict between users.
    port = np.random.randint(1025, high=65635)

    # Start building the command line that will be launched on the host
    # Open the ssh tunnel to the host
    cmd = "ssh -X -Y %s -tt -L 20001:localhost:%i %s%s << EOF\n" % \
          ("-C4c arcfour,blowfish-cbc" if not args.nocompression else "",
           port, args.username, args.host)

    # Print the hostname; for the record
    cmd += "hostname\n"

    # Add local libraries to the PATH and PYTHONPATH
    args.libs = string_to_list(args.libs)
    args.bins = string_to_list(args.bins)

    # Move to the working directory
    if args.workdir is not None:
        cmd += "if [[ ! -d %s ]]; then echo 'Error: directory %s does not exist'; exit 1; fi\n" % \
               (args.workdir, args.workdir)
        cmd += "cd %s\n" % args.workdir

    if args.mysetup is not None:
        # Use the setup file given by the user to set up the working environment (no LSST stack)
        cmd += "source %s\n" % args.mysetup
    elif args.desc:
        # Setup a DESC environment with an easy access to DESC catalogs
        desc_env = "/sps/lsst/dev/DESC/setup.sh"
        cmd += "source %s\n" % desc_env
    else:
        # Setup the lsst stack and packages if a version of the stack if given
        if args.vstack is not None:
            cmd += "source /sps/lsst/software/lsst_distrib/%s/loadLSST.bash\n" % args.vstack
        if args.packages is not None:
            cmd += ''.join(["setup %s\n" % package for package in args.packages])

        # First get the runing version of python
        if args.vstack == 'v13.0':
            cmd += "export VPY=2 \n"
            cmd += "export FVPY=2.7 \n"
        else:
            cmd += "export VPY=\`ls /sps/lsst/software/lsst_distrib/%s/python/"  % args.vstack + \
                   " | egrep -o 'miniconda[2,3]' | egrep -o '[2,3]'\`\n"
            cmd += "if [ \$VPY -eq 2 ]; then export FVPY=2.7; else export FVPY=3.6; fi\n"

        # Use default paths to make sure that jupyter is available
        jupybin = "/sps/lsst/dev/nchotard/demo/python\$VPY/bin"
        jupylib = "/sps/lsst/dev/nchotard/demo/python\$VPY/lib/python\$FVPY/site-packages"
        if args.libs is None:
            args.libs = [jupylib]
        else:
            args.libs.append(jupylib)
        if args.bins is None:
            args.bins = [jupybin]
        else:
            args.bins.append(jupybin)

        # Add ds9 to the PATH
        cmd += 'export PATH=\$PATH:/sps/lsst/dev/nchotard/local/bin\n'

        # We also need to add the following path to set up a jupyter lab
        if args.jupyter == 'lab':
            if args.labpath is not None:
                # Use the path given by the user
                cmd += 'export JUPYTERLAB_DIR="%s/share/jupyter/lab"\n' % args.labpath
            elif args.labpath is None and args.libs is not None:
                # Take the first path of the --libs list
                cmd += 'export JUPYTERLAB_DIR="%s/share/jupyter/lab"\n' % \
                       args.libs[0].split('/lib')[0]
            elif args.labpath is None and args.libs is not None:
                # That should not happen
                raise IOError("Give me a path to the install directory of jupyterlab.")

    # Add local libraries to the PATH and PYTHONPATH
    if args.libs is not None:            
        for lib in args.libs:
            cmd += 'export PYTHONPATH="\$PYTHONPATH:%s"\n' % lib
    if args.bins is not None:
        for lbin in args.bins:
            cmd += 'export PATH="\$PATH::%s"\n' % lbin

    # Launch jupyter
    cmd += 'jupyter %s --no-browser --port=%i --ip=127.0.0.1 &\n' % (args.jupyter, port)

    # Get the token number and print out the right web page to open
    cmd += "export servers=\`jupyter notebook list\`\n"
    # If might have to wait a little bit until the server is actually running...
    cmd += "while [[ \$servers != *'127.0.0.1:%i'* ]]; " % port + \
           "do sleep 1; servers=\`jupyter notebook list\`; echo \$servers; done\n"
    cmd += "export servers=\`jupyter notebook list | grep '127.0.0.1:%i'\`\n" % port
    cmd += "export TOKEN=\`echo \$servers | sed 's/\//\\n/g' | " + \
           "grep token | sed 's/ /\\n/g' | grep token \`\n"
    cmd += "printf '\\n    Copy/paste this URL into your browser to run the notebook" + \
           " localy \n\\x1B[01;92m       'http://localhost:20001/\$TOKEN' \\x1B[0m\\n\\n'\n"

    # Go back to the jupyter server
    cmd += 'fg\n'

    # And make sure we can kill it properly
    cmd += "kill -9 `ps | grep jupyter | awk '{print $1}'`\n"

    # Close
    cmd += "EOF"

    # Run jupyter
    subprocess.call(cmd, stderr=subprocess.STDOUT, shell=True)
