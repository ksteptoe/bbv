"""
To install run ``pip install .`` (or ``pip install -e .`` for editable mode)
which will install the command $(package) inside your current environment.
"""

import logging
from pathlib import Path

import click

from bbv.api import ball_map, bump_map
from bbv.Disp import Disp
from bbv.globals import BALLS, BUMPS, MARKER, X_OFFSET, Y_OFFSET
from bbv.Marker import Marker

__author__ = "Kevin Steptoe"
__copyright__ = "Kevin Steptoe"
__license__ = "MIT"

from bbv import __version__

_logger = logging.getLogger(__name__)


@click.command()
@click.argument("input_filename", type=click.Path(exists=True, readable=True))
@click.argument("output_filename", type=click.Path(), required=False)
@click.version_option(__version__, "--version")
@click.option("-v", "--verbose", "loglevel", type=int, flag_value=logging.INFO)
@click.option("-vv", "--very_verbose", "loglevel", type=int, flag_value=logging.DEBUG)
@click.option(
    "-s",
    "--sheet",
    "sheet_name",
    default="Sheet1",
    help="Sheet Name",
    show_default=True,
)
def cli(
    input_filename: Path,
    sheet_name: str = None,
    output_filename: str = None,
    loglevel=logging.INFO,
):
    """ballco

    Reads an Excel file which contains ball ordering and displays them in a plot
    Outputs ball co-ordinates
    """
    bum = bump_map(input_filename, "Bump List", output_filename, loglevel)
    ball = ball_map(input_filename, "Ball Map (2)", output_filename, loglevel)
    b_marker = Marker("BUMP", "b_", 105, -521, 6765, 1680, X_OFFSET, Y_OFFSET)
    B_marker = Marker("BALL", "B_", 0, 0, 9750, 9750)

    bumps = Disp("Bumps", BUMPS, bum, 10)
    balls = Disp("Balls", BALLS, ball, 30)
    bump_marker = Disp("BumpArea", MARKER, b_marker.marker, 5)
    ball_marker = Disp("BallArea", MARKER, B_marker.marker, 5)
    display_objects = (bumps, balls, bump_marker, ball_marker)

    action = input("b[bump] B[all] e[xpression] s[status] q[uit]?:")
    exp = ""
    while action != "q":
        if action == "b":
            bumps.toggle_state()
            bumps.status()
        elif action == "B":
            balls.toggle_state()
            balls.status()
        elif action == "s":
            for o in display_objects:
                o.status()
        elif action == "e":
            exp = input("Please Enter a Regular Expression or q[uit]?:")
            while exp != "quit" or exp != "q":
                for o in display_objects:
                    o.plot(exp)
                o.show()
                exp = input("Please Enter a Regular Expression or q[uit]?:")
                if exp == "q" or exp == "quit":
                    break
        action = input("b[bump] B[all] e[xpression] s[status] q[uit]?:")


if __name__ == "__main__":
    # ^  This is a guard statement that will prevent the following code from
    #    being executed in the case someone imports this file instead of
    #    executing it as a script.
    #    https://docs.python.org/3/library/__main__.html

    # After installing your project with pip, users can also run this Python
    # modules as scripts via the ``-m`` flag, as defined in PEP 338::
    #
    #     python -m ballco.ballco
    #
    cli()
