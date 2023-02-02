"""
To install run ``pip install .`` (or ``pip install -e .`` for editable mode)
which will install the command $(package) inside your current environment.
"""

import logging
from pathlib import Path

import click

__author__ = "Kevin Steptoe"
__copyright__ = "Kevin Steptoe"
__license__ = "MIT"

from bbv import __version__
from bbv.api import bbv_api

_logger = logging.getLogger(__name__)


@click.command()
@click.argument("input_filename", type=click.Path(exists=True, readable=True))
@click.argument("output_filename", type=click.Path(), required=False)
@click.version_option(__version__, "--version")
@click.option(
    "pcb",
    "-p",
    "--pcb",
    is_flag=True,
    show_default=True,
    default=False,
    help="PCB View flipped around x axis",
)
@click.option("-v", "--verbose", "loglevel", type=int, flag_value=logging.INFO)
@click.option("-vv", "--very_verbose", "loglevel", type=int, flag_value=logging.DEBUG)
def cli(
    input_filename: Path,
    sheet_name: str = None,
    output_filename: str = None,
    pcb: bool = False,
    loglevel=logging.INFO,
):
    """bbv

    Reads an Excel file which contains ball ordering and displays them in a plot
    Outputs ball co-ordinates
    """
    bbv_api(input_filename, output_filename, pcb, loglevel)


if __name__ == "__main__":
    # ^  This is a guard statement that will prevent the following code from
    #    being executed in the case someone imports this file instead of
    #    executing it as a script.
    #    https://docs.python.org/3/library/__main__.html

    # After installing your project with pip, users can also run this Python
    # modules as scripts via the ``-m`` flag, as defined in PEP 338::
    #
    #     python -m bbv.bbv
    #
    cli()
