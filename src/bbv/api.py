# ---- Python API ----
# The functions defined in this section can be imported by users in their
# Python scripts/interactive interpreter, e.g. via
# `from my_test_project.bbv import bbv`,
# when using this Python module as a library.

import logging
import sys

import yaml

from bbv import __version__
from bbv.ball import ball_map
from bbv.bump import bump_map
from bbv.Disp import Disp
from bbv.globals import BALLS, BUMPS, GROUP, MARKER
from bbv.Marker import Marker

_logger = logging.getLogger(__name__)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )


def bbv_api(input_filename, output_filename, pcb, group_file, loglevel):
    """Wrapper allowing :func: $(package)
    to be called with string arguments in a CLI fashion

     Args:
        input_filename:
        output_filename:
        pcb: bool
        group_file: click.File
        loglevel: int

    """
    setup_logging(loglevel)
    _logger.info(f"Version: {__version__}")

    if group_file is not None:
        try:
            group = yaml.safe_load(group_file)
        except yaml.YAMLError as exc:
            print(exc)
    else:
        group = GROUP
    bum = bump_map(input_filename, "Bump List", output_filename, loglevel)
    ball = ball_map(input_filename, "Ball Map (2)", output_filename, loglevel)
    b_marker = Marker("BUMP", "b_", bum, halo=5)
    B_marker = Marker("BALL", "B_", ball, halo=5)

    bumps = Disp("Bumps", BUMPS, bum, 10)
    balls = Disp("Balls", BALLS, ball, 30)
    bump_marker = Disp("BumpArea", MARKER, b_marker.marker, 20)
    ball_marker = Disp("BallArea", MARKER, B_marker.marker, 20)
    display_objects = (bumps, balls, bump_marker, ball_marker)

    action = input("b[bump] B[all] e[xpression] g[roup] s[status] q[uit]?:")

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
        elif action == "g":
            exp = input(
                "Please Enter a group one of: "
                + " ".join(list(group.keys()))
                + " or q[uit]?:"
            )
            while exp != "quit" or exp != "q":
                try:
                    regex = group[exp]
                    for o in display_objects:
                        o.plot(regex)
                    o.show()
                except KeyError:
                    print(f"Invalid group {exp}")
                exp = input(
                    "Please Enter a group one of: "
                    + " ".join(list(group.keys()))
                    + " or q[uit]?:"
                )
                if exp == "q" or exp == "quit":
                    break
        action = input("b[bump] B[all] e[xpression] g[roup] s[status] q[uit]?:")

    _logger.info("Script ends here")
