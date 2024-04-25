"""
Lightweight bootstrapping for project scripts
"""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("sandal")
except PackageNotFoundError:
    # package is not installed
    pass
