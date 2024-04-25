import logging
from typing import TypeAlias

Verbosity: TypeAlias = int | bool | None


def vrb_to_level(verbose: Verbosity) -> int:
    if verbose is None:
        verbose = 0
    if verbose is True:
        verbose = 1

    level = logging.INFO
    if verbose < 0:
        level = logging.WARN
    elif verbose > 0:
        level = logging.DEBUG
    return level
