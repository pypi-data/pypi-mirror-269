"""
Setup routines for CLI environments.
"""

import logging
import sys
from pathlib import Path

import progress_api
from colorlog import ColoredFormatter
from enlighten import Manager
from progress_api.backends.enlighten import EnlightenProgressBackend

from .loghelper import Verbosity, vrb_to_level

term_fmt = ColoredFormatter(
    "[%(blue)s%(asctime)s%(reset)s] %(log_color)s%(levelname)-8s%(reset)s %(cyan)s%(logger)s %(blue)s%(message)s",  # noqa: E501
    datefmt="%H:%M:%S",
    reset=True,
    log_colors={
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "red,bg_white",
    },
    secondary_log_colors={},
    style="%",
)

file_fmt = logging.Formatter(
    "[%(asctime)s] %(levelname)-8s %(processName)s %(logger)s %(message)s",
)


def setup_logging(
    verbose: Verbosity = None,
    log_file: str | Path | None = None,
    log_file_verbose: Verbosity = None,
):
    """
    Initialize logging and progress bars for a CLI environment.

    Args:
        verbose: whether to include debug output.
        log_file: a log file to write to.
        log_file_verbose: override ``verbose`` for the log file.
    """
    global emgr

    term_level = vrb_to_level(verbose)

    handler = logging.StreamHandler(stream=sys.stderr)
    handler.setFormatter(term_fmt)
    handler.setLevel(term_level)
    root = logging.getLogger()
    root.addHandler(handler)
    if log_file:
        if log_file_verbose is not None:
            file_level = vrb_to_level(log_file_verbose)
        else:
            file_level = term_level
        root.setLevel(min(term_level, file_level))
        fh = logging.FileHandler(log_file, mode="w")
        fh.setLevel(file_level)
        fh.setFormatter(file_fmt)
        root.addHandler(fh)
    else:
        root.setLevel(term_level)

    emgr = Manager(stream=sys.stderr)
    progress_api.set_backend(EnlightenProgressBackend, emgr)
