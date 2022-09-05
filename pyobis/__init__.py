"""
pyobis library
~~~~~~~~~~~~~~~~~~~~~

pyobis is a Python client for OBIS.

Example usage:

# Import entire library
import pyobis
# or import modules as needed
## occurrence
from pyobis import occurrence
## taxa
from pyobis import taxa
## dataset
from pyobis import dataset
## checklist
from pyobis import checklist

## use advanced logging
### setup first
import requests
import logging
import httplib as http_client
http_client.HTTPConnection.debuglevel = 1
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True
### then make request
from pyobis import occurrence
occurrence.search(geometry='POLYGON((30.1 10.1, 10 20, 20 40, 40 40, 30.1 10.1))')
"""

try:
    from ._version import __version__
except ImportError:
    __version__ = "unknown"

__title__ = "pyobis"
__author__ = "pyOBIS Community"
__license__ = "MIT"

from .checklist import checklist
from .dataset import dataset
from .nodes import nodes
from .occurrences import occurrences
from .taxa import taxa

__all__ = [
    "checklist",
    "dataset",
    "nodes",
    "occurrences",
    "taxa",
]
