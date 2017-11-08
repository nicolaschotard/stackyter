#!/usr/bin/env python
"""Run jupyter at CC-IN2P3, setup the LSST stack, and display it localy."""


import sys
import subprocess
from argparse import ArgumentParser
from argparse import ArgumentDefaultsHelpFormatter
import yaml
import numpy as np


def string_to_list(a):
    """Transform a string with coma separated values to a list of values."""
    return a if isinstance(a, list) or a is None else a.split(",")


if __name__ == '__main__':

    description = """Run Jupyter on CC-IN2P3, setup the LSST stack, and display it localy."""
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
    parser.add_argument("--workdir", default='/pbs/throng/lsst/users/<username>/notebooks',
                        help="Your working directory at CC-IN2P3")
    parser.add_argument("--vstack", default='v14.0',
                        help="Version of the stack you want to set up."
                        " (E.g. v14.0, w_2017_43 or w_2017_43_py2)")
    parser.add_argument("--packages", default='lsst_distrib',
                        help="A list of packages you want to setup. Coma separated from command"
                        " line, or a list in the config file. You can use the `lsst_distrib` "
                        "package to set up all available packages from a given distrib.")
    parser.add_argument("--jupyter", default="notebook",
                        help="Either launch a jupiter notebook or a jupyter lab.")
    parser.add_argument("--cca", default="cca7",
                        help="Either connect to ccage or cca7. ccage might be used for old or local"
                        " install of the stack, whereas all newer versions (>= v13.0, installed "
                        "for the LSST group) must be set up on centos7 (cca7).")
    parser.add_argument("--libs", default=None,
                        help="Path(s) to local Python librairies. Will be added to your PYTHONPATH."
                        " Coma separated to add more than one paths, or a list in the config file."
                        " A default path for jupyter will be choose if not given.")
    parser.add_argument("--bins", default=None,
                        help="Path(s) to local binaries. Will be added to your PATH."
                        " Coma separated to add more than one paths, or a list in the config file."
                        " A default path for jupyter will be choose if not given.")
    parser.add_argument("--labpath", default=None,
                        help="You must provide the path in which jupyterlab has been installed"
                        " in case it differs from the (first) path you gave to the --libs option."
                        " A default path for jupyterlab will be choose if not given.")
    args = parser.parse_args()

    # Check if a configuration file is given
    if args.config is not None:
        config = yaml.load(open(args.config, 'r'))
        for opt, val in args._get_kwargs():
            # only keep option value from the config file
            # if the user has not set it up from command line
            if opt in config and '--' + opt not in sys.argv:
                setattr(args, opt, config[opt])

    # A valid username (and the corresponding password) is actually the only mandatory thing we need
    if args.username is None:
        raise IOError("You must give you CC-IN2P3 username through the '--username' option.")

    # Make sure that we have a list (even empty) for packages
    args.packages = string_to_list(args.packages)

    # A random port number is selected between 1025 and 65635 (included) for server side to
    # prevent from conflict between users.
    port = np.random.randint(1025, high=65635)

    # Start building the command line that will be launched at CC-IN2P3
    # Open the ssh tunnel to a CC-IN2P3 host
    cmd = "ssh -X -YC4c arcfour,blowfish-cbc -tt -L 20001:localhost:%i %s@%s.in2p3.fr << EOF\n" % \
          (port, args.username, args.cca)

    # Print the hostname; for the record
    cmd += "hostname\n"

    # Setup the lsst stack and packages if a version of the stack if given
    if args.vstack is not None:
        cmd += "source /sps/lsst/software/lsst_distrib/%s/loadLSST.bash\n" % args.vstack
    if args.packages is not None:
        cmd += ''.join(["setup %s\n" % package for package in args.packages])

    # Add local libraries to the PATH and PYTHONPATH
    args.libs = string_to_list(args.libs)
    args.bins = string_to_list(args.bins)

    # First get the runing version of python
    if args.vstack == 'v13.0':
        cmd += "export VPY=2 \n"
        cmd += "export FVPY=2.7 \n"
    else:
        cmd += "export VPY=\`ls /sps/lsst/software/lsst_distrib/%s/python/"  % args.vstack + \
               " | egrep -o 'miniconda[2,3]' | egrep -o '[2,3]'\`\n"
        cmd += "if [ \$VPY -eq 2 ]; then export FVPY=2.7; else export FVPY=3.6; fi\n"

    # Use default paths to make sure that jupyter is available
    if args.libs is None:
        args.libs = ['/sps/lsst/dev/nchotard/demo/python\$VPY/lib/python\$FVPY/site-packages']
    if args.bins is None:
        args.bins = ["/sps/lsst/dev/nchotard/demo/python\$VPY/bin"]
    for lib in args.libs:
        cmd += 'export PYTHONPATH="%s:\$PYTHONPATH"\n' % lib
    for lbin in args.bins:
        cmd += 'export PATH="%s:\$PATH:"\n' % lbin

    # Add ds9 to the PATH
    cmd += 'export PATH=\$PATH:/sps/lsst/dev/nchotard/local/bin\n'

    # We also need to add the following path to set up a jupyter lab
    if args.jupyter == 'lab':
        if args.labpath is not None:
            # Use the path given by the user
            cmd += 'export JUPYTERLAB_DIR="%s/share/jupyter/lab"\n' % args.labpath
        elif args.labpath is None and args.libs is not None:
            # Take the first path of the --libs list
            cmd += 'export JUPYTERLAB_DIR="%s/share/jupyter/lab"\n' % args.libs[0].split('/lib')[0]
        elif args.labpath is None and args.libs is not None:
            # That should not happen
            raise IOError("Give me a path to the directory in which jupyterlab has been installed.")

    # Move to the working directory
    if args.workdir == '/pbs/throng/lsst/users/<username>/notebooks':
        args.workdir = args.workdir.replace('<username>', args.username)
    cmd += "cd %s\n" % args.workdir

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
