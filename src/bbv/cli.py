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
@click.argument("pcs_filename", type=click.Path(exists=True, readable=True))
@click.argument("sondrel_filename", type=click.Path(exists=True, readable=True))
@click.option(
    "-g", "--group", "group", type=click.File(mode="r"), required=False, default=None
)
@click.option("-p", "--pcs_row_offset", type=int, required=False, default=4)
@click.option("-u", "--pcs_sheet_name", type=str, required=False, default="Data")
@click.option(
    "-a", "--sondrel_sheet_name", type=str, required=False, default="Ball Map 2"
)
@click.option("-s", "--sondrel_row_offset", type=int, required=False, default=2)
@click.option("-v", "--verbose", "loglevel", type=int, flag_value=logging.INFO)
@click.version_option(__version__, "--version")
def cli(
    pcs_filename: Path,
    sondrel_filename: Path,
    group: click.File,
    pcs_row_offset: int,
    pcs_sheet_name: str,
    sondrel_sheet_name: str,
    sondrel_row_offset: int,
    loglevel=logging.INFO,
):
    bbv_api(
        pcs_filename,
        sondrel_filename,
        group,
        pcs_row_offset,
        sondrel_row_offset,
        loglevel,
        pcs_sheet_name,
        sondrel_sheet_name,
    )


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
