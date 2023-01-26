"""
To install run ``pip install .`` (or ``pip install -e .`` for editable mode)
which will install the command $(package) inside your current environment.
"""

import logging
from pathlib import Path

import click
import matplotlib.pylab as plt
import pandas as pd

from ballco.api import ball_map, bump_map
from ballco.globals import X_OFFSET, Y_OFFSET

__author__ = "Kevin Steptoe"
__copyright__ = "Kevin Steptoe"
__license__ = "MIT"

from ballco import __version__

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

    Reads an Excel file which contains ball ordering
    Outputs ball co-ordinates
    """
    bum = bump_map(input_filename, "Bump List", output_filename, loglevel)
    ball = ball_map(input_filename, "Ball Map", output_filename, loglevel)
    bum_ball = pd.concat([bum, ball], ignore_index=True)
    bumps_on = True
    balls_on = True
    action = input("b[bump] B[all] e[xpression] s[status] q[uit]?:")
    exp = ""
    b_marker = pd.DataFrame(
        {"Chip Ball Name": ["b_LL", "b_UR"], "x": [105, 6765], "y": [-521, 1680]}
    )
    b_marker.x += X_OFFSET
    b_marker.y += Y_OFFSET
    B_marker = pd.DataFrame(
        {"Chip Ball Name": ["B_LL", "B_UR"], "x": [26105, 32765], "y": [64479, 66680]}
    )

    while action != "q":
        if action == "b":
            bumps_on = not bumps_on
            print(f"Bumps On {bumps_on}")
        elif action == "B":
            balls_on = not balls_on
            print(f"Balls On {balls_on}")
        elif action == "s":
            print(f"Bumps On {bumps_on} Balls On {balls_on} regex ->{exp}<-")
        elif action == "e":
            exp = input("Please Enter a Regular Expression or q[uit]?:")
            while exp != "quit" or exp != "q":
                try:
                    disp = bum_ball[bum_ball["Chip Ball Name"].str.match(exp)]
                    balls = disp[disp["TYPE"] == "BALL"]
                    bumps = disp[disp["TYPE"] == "BUMP"]
                    types = [b_marker, B_marker]
                    if bumps_on:
                        types.append(bumps)
                    if balls_on:
                        types.append(balls)
                    for type in types:
                        plt.scatter(type.x, type.y)
                        for index, row in type.iterrows():
                            plt.annotate(row[0], (row.x, row.y + 300))
                    plt.show()
                except Exception as e:
                    click.echo(
                        click.style(
                            "{} Error on processing regex: {}".format(str(e), exp),
                            fg="red",
                        )
                    )
                exp = input("Please Enter a Regular Expression or q[uit]?:")
                if exp == "q" or exp == "quit":
                    break
        action = input("b[bump] B[all] e[xpression] q[uit]?:")


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
