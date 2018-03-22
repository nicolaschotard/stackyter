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


def setup_parser():
    description = "Run Jupyter on a distant host and display it localy."
    prog = "stackyter.py"
    usage = """%s [options]""" % prog

    parser = ArgumentParser(prog=prog, usage=usage, description=description,
                            formatter_class=ArgumentDefaultsHelpFormatter)

    # General options
    parser.add_argument('-c', '--config', default=None,
                        help='Name of the configuration to use, taken from your default '
                        'configuration file (~/.stackyter-config.yaml or $STACKYTERCONFIG). '
                        "Default if to use the 'default_config' defined in this file. "
                        'The content of the configuration file will be overwritten by any '
                        'given command line options.')
    parser.add_argument('-f', '--configfile', default=None,
                        help='Configuration file containing a set of option values. The content '
                        'of this file will be overwritten by any given command line options.')
    parser.add_argument('-H', "--host", default="cca7.in2p3.fr",
                        help="Name of the target host. Allows you to avoid conflit with the "
                        "content of your $HOME/.ssh/config, or to connect to any host on which "
                        "Jupyter is available.")
    parser.add_argument('-u', '--username',
                        help="Your user name on the host. If not given, ssh will try to "
                        "figure it out from you ~/.ssh/config or will use your local user name.")
    parser.add_argument('-w', "--workdir", default=None,
                        help="Your working directory on the host")
    parser.add_argument("--mysetup", default=None,
                        help="Path to a setup file (on the host) that will be used to set up the "
                        "working environment. A Python installation with Jupyter must be "
                        "available to make this work.")
    parser.add_argument('-j', "--jupyter", default="notebook",
                        help="Either launch a jupiter notebook or a jupyter lab.")
    parser.add_argument("--runbefore", default=None,
                        help="A list of extra commands to run BEFORE sourcing your setup file."
                        " Coma separated for more than one command, or a list in the config file.")
    parser.add_argument("--runafter", default=None,
                        help="A list of extra commands to run AFTER sourcing your setup file."
                        " Coma separated for more than one command, or a list in the config file.")
    parser.add_argument('-C', '--compression', action='store_true', default=False,
                        help='Activate ssh compression option (-C).')
    parser.add_argument('-S', '--showconfig', action='store_true', default=False,
                        help='Show all available configurations from your default file and exit.')

    return parser


def main():
    parser = setup_parser()
    args = parser.parse_args()
    default_args = parser.parse_args(args=[])

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
            if opt in config and args.__dict__[opt] == default_args.__dict__[opt]:
                setattr(args, opt, config[opt])

    # A valid username (and the corresponding password) is actually the only mandatory thing we need
    args.username = "" if args.username is None else args.username + "@"

    # Make sure that we have a list (even empty) for extra commands to run
    args.runbefore = string_to_list(args.runbefore)
    args.runafter = string_to_list(args.runafter)

    # A random port number is selected between 1025 and 65635 (included) for server side to
    # prevent from conflict between users.
    port = np.random.randint(1025, high=65635)

    # Start building the command line that will be launched on the host
    # Open the ssh tunnel to the host
    cmd = "ssh -X -Y %s -tt -L 20001:localhost:%i %s%s << EOF\n" % \
          ("-C" if args.compression else "", port, args.username, args.host)

    # Move to the working directory
    if args.workdir is not None:
        cmd += "if [[ ! -d %s ]]; then echo 'Error: directory %s does not exist'; exit 1; fi\n" % \
               (args.workdir, args.workdir)
        cmd += "cd %s\n" % args.workdir

    # Do we have to run something before sourcing the setup file
    if args.runbefore:
        cmd += ''.join([run.replace("$", "\$") + "\n" for run in args.runbefore])
    if args.mysetup is not None:
        # Use the setup file given by the user to set up the working environment
        cmd += "source %s\n" % args.mysetup
    if args.runafter:
        cmd += ''.join([run.replace("$", "\$") + "\n" for run in args.runafter])

    # Launch jupyter
    cmd += 'jupyter %s --no-browser --port=%i --ip=127.0.0.1 &\n' % (args.jupyter, port)

    # Get the token number and print out the right web page to open
    cmd += "export servers=\`jupyter notebook list\`\n"
    # If might have to wait a little bit until the server is actually running...
    cmd += "while [[ \$servers != *'127.0.0.1:%i'* ]]; " % port + \
           "do sleep 1; servers=\`jupyter notebook list\`; echo waiting...; done\n"
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
