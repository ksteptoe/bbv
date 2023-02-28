# ---- Python API ----
# The functions defined in this section can be imported by users in their
# Python scripts/interactive interpreter, e.g. via
# `from my_test_project.bbv import bbv`,
# when using this Python module as a library.

import logging
import sys
from collections import namedtuple

import yaml

from bbv import __version__
from bbv.ball import ball_map
from bbv.bump import bump_map
from bbv.BvBChecker import BvBCHeck
from bbv.Disp import Disp
from bbv.globals import BALLS, BUMPS, GROUP, MARKER
from bbv.Marker import Marker

DataSet = namedtuple(
    "DataSet",
    [
        "pcs_filename",
        "pcs_sheetname",
        "pcs_rowoffset",
        "sondrel_filename",
        "sondrel_sheetname",
        "sondrel_rowoffset",
    ],
)
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


def bbv_api(
    pcs_filename,
    sondrel_filename,
    group_file,
    pcs_rowoffset,
    sondrel_rowoffset,
    loglevel,
    pcs_sheetname,
    sondrel_sheetname,
):
    """Wrapper allowing :func: $(package)
    to be called with arguments in a CLI fashion

     Args:
        pcs_filename: Path
        sondrel_filename: Path
        group_file: click.File
        rows: int
        loglevel: int
        pcs_rowoffset: int
        sondrel_rowoffset: int
        pcs_sheetname: str
        sondrel_sheetname: str

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
    bum = bump_map(pcs_filename, pcs_sheetname, pcs_rowoffset)
    bum.to_pickle("bum.pckl")
    ball = ball_map(sondrel_filename, sondrel_sheetname, sondrel_rowoffset)
    ball.to_pickle("ball.pckl")
    data_set = DataSet(
        pcs_filename,
        pcs_sheetname,
        pcs_rowoffset,
        sondrel_filename,
        sondrel_sheetname,
        sondrel_rowoffset,
    )
    b_marker = Marker("BUMP", "b_", bum, halo=5)
    B_marker = Marker("BALL", "B_", ball, halo=5)

    bumps = Disp("Bumps", BUMPS, bum, 10)
    balls = Disp("Balls", BALLS, ball, 30)
    bump_marker = Disp("BumpArea", MARKER, b_marker.marker, 20)
    ball_marker = Disp("BallArea", MARKER, B_marker.marker, 20)
    display_objects = (bumps, balls, bump_marker, ball_marker)

    action = input("b[bump] B[all] e[xpression] g[roup] s[status] c[check] q[uit]?:")

    exp = ""
    while action != "q":
        if action == "b":
            bumps.toggle_state()
            bumps.status()
        elif action == "B":
            balls.toggle_state()
            balls.status()
        elif action == "c":
            bvbchecker = BvBCHeck(ball, bum, data_set)
            bvbchecker.report()
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
        action = input("b[bump] B[all] e[xpression] g[roup] s[status] c[heck] q[uit]?:")

    _logger.info("Script ends here")
