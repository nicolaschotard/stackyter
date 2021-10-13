#!/usr/bin/env python
"""Run jupyter on a given host and display it localy."""

import os
import sys
import subprocess
from argparse import ArgumentParser
from argparse import ArgumentDefaultsHelpFormatter
import yaml
import random 


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
    return yaml.load(open(config, 'r'), Loader=yaml.SafeLoader) if not only_path else config


def read_config(config, key=None):
    """Read a config file and return the right configuration."""
    print("INFO: Loading configuration from", config)
    config = yaml.load(open(config, 'r'), Loader=yaml.SafeLoader)
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
    description = """Run Jupyter on a distant host and display it localy."""
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
    parser.add_argument('-H', "--host", default=None,
                        help="Name of the target host. Allows you to connect to any host "
                        "on which Jupyter is available, or to avoid conflit with the "
                        "content of your $HOME/.ssh/config.")
    parser.add_argument('-u', '--username',
                        help="Your user name on the host. If not given, ssh will try to "
                        "figure it out from you ~/.ssh/config or will use your local user name.")
    parser.add_argument('-J', '--jump', default=None,
                        help="jump hosts or gateways in the form username@host. For serveral hops,"
                             " give them ordered and separated by a coma.")
    parser.add_argument('-w', "--workdir", default="$HOME",
                        help="Your working directory on the remote host")
    parser.add_argument('-j', "--jupyter", default="notebook",
                        help="Either launch Jupyter notebook or Jupyter lab.")
    parser.add_argument("--mysetup", default=None,
                        help="Path to a setup file (on the host) that will be used to set up the "
                        "working environment. A Python installation with Jupyter must be "
                        "available to make this work.")
    parser.add_argument("--runbefore", default=None,
                        help="A list of extra commands to run BEFORE sourcing your setup file."
                        " Coma separated for more than one commands, or a list in the config file.")
    parser.add_argument("--runafter", default=None,
                        help="A list of extra commands to run AFTER sourcing your setup file."
                        " Coma separated for more than one commands, or a list in the config file.")
    parser.add_argument('-C', '--compression', action='store_true', default=False,
                        help='Activate ssh compression option (-C).')
    parser.add_argument('-S', '--showconfig', action='store_true', default=False,
                        help='Show all available configurations from your default file and exit.')
    parser.add_argument('--localport', default=20001, type=int,
                        help="Local port to use to connect to the distant machine."
                        "The default value is 20001.")

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

    # Do we have a valid host name
    if args.host is None:
        raise ValueError("You must give a valid host name (--host)")

    # Do we have a valid username
    args.username = "" if args.username is None else args.username + "@"

    # Do we have a valid Jupyter flavor
    if args.jupyter not in ("notebook", "lab"):
        raise ValueError(f"Invalid Jupyter flavor '{args.jupyter}': expecting either 'notebook' or 'lab'")

    # Make sure that we have a list (even empty) for extra commands to run
    args.runbefore = string_to_list(args.runbefore)
    args.runafter = string_to_list(args.runafter)

    # A random port number is selected between 1025 and 65635 (included) for server side to
    # prevent from conflict between users.
    port = random.randint(1025, 65635)

    # Should we use a jump host?
    jumphost = f"-J {args.jump}" if args.jump else ""

    # Do we have to run something before sourcing the setup file ?
    run_before = ''.join([run.replace("$", "\$") + "; " for run in args.runbefore]) if args.runbefore else ""

    # Do we have to run something after sourcing the setup file ?
    run_after = ''.join([run.replace("$", "\$") + "; " for run in args.runafter]) if args.runafter else ""

    # Use the setup file given by the user to set up the working environment
    user_setup = f"source {args.mysetup}" if args.mysetup else ""

    script = f"""
        #!/bin/bash
        if [[ ! -d {args.workdir} ]]; then
            echo 'Error: directory {args.workdir} does not exist'
            exit 1
        fi
        cd {args.workdir}
        {run_before}
        {user_setup}
        {run_after}
        jupyter_version=$(jupyter --version | grep '{args.jupyter}' | awk '{{print $NF}}' | awk -F '.' '{{print $1}}')
        function get_servers() {{
            local version=$1
            local flavor="{args.jupyter}"
            local servers=""
            local cmd="echo"
            case ${{flavor}} in
            notebook)
                cmd="jupyter notebook list"
                ;;
            lab)
                if [[ $version -le 2 ]]; then
                    cmd="jupyter notebook list"
                else
                    cmd="jupyter server list"
                fi
                ;;
            esac
            echo `$cmd 2> /dev/null | grep '127.0.0.1:{port}' `
        }}
        set -m    # For job control
        jupyter {args.jupyter} --no-browser --port={port} --ip=127.0.0.1 &
        jupyter_pid=$!
        for i in $(seq 1 10); do
            sleep 2s
            servers=$(get_servers $jupyter_version)
            if [[ $servers == *"127.0.0.1:{port}"* ]]; then
                break
            fi
            echo 'waiting...'
        done
        if [[ -z ${{servers}} ]]; then
           echo 'could not determine the URL of the Jupyter server'
           kill -TERM ${{jupyter_pid}} &> /dev/null
           exit 1
        fi
        token=$(echo $servers | grep token | sed 's|^http.*?token=||g' | awk '{{print $1}}')
        printf "\nCopy/paste the URL below into your browser to open your notebook \n\n\\x1B[01;92m    http://localhost:{args.localport}/?token=%s \\x1B[0m\\n\\n" $token
        fg
        kill -TERM ${{jupyter_pid}} &> /dev/null
        exit 0
    """

    # Establish the SSH tunnel and run the shell script
    cmd = f"ssh {jumphost} -X -Y {'-C' if args.compression else ''} -tt -L {args.localport}:localhost:{port} {args.username}{args.host}"
    proc = subprocess.run(cmd, input=script.encode(), stderr=subprocess.STDOUT, shell=True)
    sys.exit(proc.returncode)
