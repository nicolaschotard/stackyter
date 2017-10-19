#!/usr/bin/env python
"""Run a jupyter at CC-IN2P3, setup the LSST stack, and display it localy."""


import sys
import subprocess
from argparse import ArgumentParser
from argparse import ArgumentDefaultsHelpFormatter
import yaml


if __name__ == '__main__':

    description = """Run Jupyter on CC-IN2P3, setup the LSST stack, and display it localy.

    This script will allow you to run a jupyter notebook (or lab) at CC-IN2P3 while displaying it
    localy in your favorite brower. It is mainly intended to help LSST members to interact with the
    datasets already available at CC-IN2P3 using Python. But setting up the LSST stack is not mandatory,
    making this script useful in other (LSST) contexts.
    """
    prog = "stackyter.py"
    usage = """%s [options]""" % prog

    parser = ArgumentParser(prog=prog, usage=usage, description=description,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('--config',
                        help='Configuration file containing a set of option values. '
                        'The content of this file will be overwritten by any given'
                        ' command line options.')
    parser.add_argument('--username', help='Your CC-IN2P3 user name. Mandatory '
                        'either from command line or in the configuration file.')
    parser.add_argument("--workdir", default='\$HOME',
                        help="Your working directory at CC-IN2P3")
    parser.add_argument("--vstack",
                        help="Version of the stack you want to setup up."
                        " If not given, the LSST stack will not be set up.")
    parser.add_argument("--packages", default=None,
                        help="A list of packages you want to setup. Coma separated"
                        " from command line, or a list in the config file.")
    parser.add_argument("--jupyter", default="notebook",
                        help="Either launch a jupiter notebook or a jupyter lab.")
    parser.add_argument("--cca", default="cca7",
                        help="Either connect to ccage or cca7. ccage might be used"
                        " for old versions of the stack, whereas all newer versions"
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
    cmd = "ssh -tt -L 20001:localhost:20002 %s@%s.in2p3.fr << EOF\n" % \
          (args.username, args.cca)

    # Print the hostname; for the record
    cmd += "hostname\n"

    # Setup the lsst stack and packages if a version of the stack if given
    if args.vtack is not None:
        cmd += "source /sps/lsst/software/lsst_distrib/%s/loadLSST.bash\n" % args.vstack
        cmd += ''.join(["setup %s\n" % package for package in args.packages])

    # Add local libraries to the PATH and PYTHONPATH
    cmd += 'export PYTHONPATH="/sps/lsst/dev/nchotard/demo/python3/lib/python3.6/site-packages:\$PYTHONPATH"\n'
    cmd += 'export PATH="/sps/lsst/dev/nchotard/demo/python3/bin:\$PATH:"\n'
    if args.jupyter == 'lab':
        cmd += 'export JUPYTERLAB_DIR="/sps/lsst/dev/nchotard/demo/python3/share/jupyter/lab"\n'

    # Move to the working directory
    cmd += "cd %s\n" % args.workdir

    # Launch jupyter
    cmd += 'jupyter %s --no-browser --port=20002 --ip=127.0.0.1 &\n' % args.jupyter

    # Get the token number and print out the right web page to open
    cmd += "export servers=\`jupyter notebook list\`\n"
    cmd += "while [[ \$servers != *'127.0.0.1:20002'* ]]; do sleep 1; servers=\`jupyter notebook list\`; echo \$servers; done\n"
    cmd += "export servers=\`jupyter notebook list | grep '127.0.0.1:20002'\`\n"
    cmd += "export TOKEN=\`echo \$servers | sed 's/\//\\n/g' | grep token | sed 's/ /\\n/g' | grep token \`\n"
    cmd += "echo -e '\\x1B[01;94m    Copy/paste this URL into your browser to run the notebook localy 'http://localhost:20001/\$TOKEN' \\x1B[0m'\n"

    # Go back to the jupyter server
    cmd += 'fg\n'

    # And make sure we can kill it properly
    cmd += "kill -9 `ps | grep jupyter | awk '{print $1}'`\n"

    # Close
    cmd += "EOF"

    # Run jupyter
    subprocess.call(cmd, stderr=subprocess.STDOUT, shell=True)
