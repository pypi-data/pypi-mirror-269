CLI Helpers
===========

.. py:module:: sandal.cli

These functions help run CLI programs.

Logging
-------

This quickly initializes the Python logging infrastructure and sets up
:py:mod:`progress_api` to use Enlighten_ as its backend.

.. _Enlighten: https://python-enlighten.readthedocs.io/en/stable/index.html

.. autofunction:: setup_logging
