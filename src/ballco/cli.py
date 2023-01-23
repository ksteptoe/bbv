"""
To install run ``pip install .`` (or ``pip install -e .`` for editable mode)
which will install the command $(package) inside your current environment.
"""

import logging
import click
from .api import ballco_api

__author__ = "Kevin Steptoe"
__copyright__ = "Kevin Steptoe"
__license__ = "MIT"

from ballco import __version__

_logger = logging.getLogger(__name__)


@click.command()
@click.version_option(__version__, '--version')
@click.argument('n', type=int)
@click.option('-v', '--verbose', 'loglevel', type=int, flag_value=logging.INFO)
@click.option('-vv', '--very_verbose', 'loglevel', type=int, flag_value=logging.DEBUG)
def cli(n, loglevel):
    """Calls :func:`main` passing the CLI arguments extracted from click

    This function can be used as entry point to create console scripts with setuptools.
    """
    ballco_api(n, loglevel)


if __name__ == "__main__":
    # ^  This is a guard statement that will prevent the following code from
    #    being executed in the case someone imports this file instead of
    #    executing it as a script.
    #    https://docs.python.org/3/library/__main__.html

    # After installing your project with pip, users can also run this Python
    # modules as scripts via the ``-m`` flag, as defined in PEP 338::
    #
    #     python -m ballco.ballco 42
    #
    cli()
