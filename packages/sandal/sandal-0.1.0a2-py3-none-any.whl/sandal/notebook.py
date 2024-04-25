"""
Setup routines for CLI environments.
"""

import logging
import sys

from .loghelper import Verbosity, vrb_to_level

_log_initialized = False

nb_fmt = logging.Formatter(
    "[%(asctime)s] %(levelname)-8s %(logger)s %(message)s",
)


def setup_logging(verbose: Verbosity):
    """
    Set up logging for a notebook environment.

    Args:
        verbose: the verbosity level.
    """
    global _log_initialized
    level = vrb_to_level(verbose)
    root = logging.getLogger()

    if not _log_initialized:
        handler = logging.StreamHandler(stream=sys.stderr)
        handler.setFormatter(nb_fmt)
        root.addHandler(handler)
        _log_initialized = True

    root.setLevel(level)
