#!/usr/bin/env python
"""Run a jupyter at CC-IN2P3, setup the LSST stack, and display it localy."""


import sys
import subprocess
from argparse import ArgumentParser
from argparse import ArgumentDefaultsHelpFormatter
import yaml


if __name__ == '__main__':

    description = """Run Jupyter on CC-IN2P3, setup the LSST stack, and display it localy."""
    prog = "stackyter.py"
    usage = """%s [options]""" % prog

    parser = ArgumentParser(prog=prog, usage=usage, description=description,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('--config',
                        help='Configuration file containing a set of option values. '
                        'The content of this file will be overwritten by any given'
                        ' command line option values shown below.')
    parser.add_argument('--username', help='Your CC-IN2P3 user name. Mandatory '
                        'either from command line or in the configuration file.')
    parser.add_argument("--workdir", default='\$HOME',
                        help="Your working directory at CC-IN2P3")
    parser.add_argument("--vstack", default='w_2017_38',
                        help="Version of the stack you want to setup up.")
    parser.add_argument("--packages", default=None,
                        help="A list of packages you want to setup. Coma separated"
                        " from command line, or a list in the config file.")
    parser.add_argument("--jupyter", default="notebook",
                        help="Either launch a jupiter notebook or a jupyter lab.")
    parser.add_argument("--cca", default="cca7",
                        help="Either connecte to ccage or cca7. ccage might be used"
                        " for old version of the stack, whereas all newer version"
                        " (>v13) must be set up on centos7 (cca7).")
    args = parser.parse_args()

    # Check if a configuration file is given
    if args.config is not None:
        config = yaml.load(open(args.config, 'r'))
        for opt, val in args._get_kwargs():
            # only keep option value from the config file
            # if the user has not set it up from command line
            if opt in config and '--' + opt not in sys.argv:
                setattr(args, opt, config[opt])

    # A proper username is actually the only mandatory thing we need
    if args.username is None:
        raise IOError("Option 'username' is mandatory.")

    # Make sure that we have a list (even empty) for packages
    args.packages = args.packages if isinstance(args.packages, list) else args.packages.split(",")

    # Start building the command line that will be launched at CC-IN2P3
    # Open the ssh tunnel to a CC-IN2P3 host
#    cmd = "xdg-open http://localhost:20001/tree &\n"
    cmd = "ssh -tt -L 20001:localhost:20002 %s@%s.in2p3.fr << EOF\n" % \
          (args.username, args.cca)

    # Print the hostname; for the record
    cmd += "hostname\n"

    # Setup the lsst stack and packages
    cmd += "source /sps/lsst/software/lsst_distrib/%s/loadLSST.bash\n" % args.vstack
    cmd += ''.join(["setup %s\n" % package for package in args.packages])

    # Add local libraries to the PATH and PYTHOPATh
    cmd += 'export PYTHONPATH="/sps/lsst/dev/nchotard/demo/python3/lib/python3.6/site-packages:\$PYTHONPATH"\n'
    cmd += 'export PATH="/sps/lsst/dev/nchotard/demo/python3/bin:\$PATH:"\n'
    cmd += 'export JUPYTERLAB_DIR="/sps/lsst/dev/nchotard/demo/python3/share/jupyter/lab"\n'
    # Move to the working directory
    cmd += "cd %s\n" % args.workdir

    # Launch jupyter
    cmd += 'jupyter %s --no-browser --port=20002 --ip=127.0.0.1\n' % args.jupyter

    # Make sure we can kill it properly
    cmd += "kill -9 `ps | grep jupyter | awk '{print $1}'`\n"

    # Close
    cmd += "EOF"

    # Run jupyter
    subprocess.call(cmd, stderr=subprocess.STDOUT, shell=True)