"""
stackyter - Local display of a jupyter notebook running on a remote server
Licensed under a MIT style license - see LICENSE file
"""

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("stackyter")
except PackageNotFoundError:
    raise PackageNotFoundError from None
