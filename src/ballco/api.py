# ---- Python API ----
# The functions defined in this section can be imported by users in their
# Python scripts/interactive interpreter, e.g. via
# `from my_test_project.ballco import ballco`,
# when using this Python module as a library.

import logging
import sys

import click
import pandas as pd

# Todo get version working
# from ballco import __version__
from ballco.globals import PITCH, X_BUMP_OFFSET, X_OFFSET, Y_BUMP_OFFSET, Y_OFFSET

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


# def ballco_api(input_filename, sheet_name, output_filename, loglevel):
#     """Wrapper allowing :func: $(package)
#     to be called with string arguments in a CLI fashion
#
#      Args:
#         input_filename:
#         sheet_name:
#         output_filename:
#         loglevel: int
#
#     """
#     setup_logging(loglevel)
#     _logger.info(f"Version: {__version__}")
#     ballco(input_filename, sheet_name, output_filename, test)
#     _logger.info("Script ends here")


def bump_map(input_filename, sheet_name, output_filename, loglevel):
    """bump_map

    Args:
       input_filename:
       output_filename:
       sheet_name:
       output_filename:
       loglevel: int
    """

    if output_filename is None:
        output_filename = input_filename
    df = pd.DataFrame()
    try:
        df = pd.read_excel(input_filename, sheet_name=sheet_name, skiprows=4)
    except Exception as e:  # noqa: F841
        click.echo(
            click.style("f{str(e)} Error on processing {input_filename}", fg="red")
        )
        exit(1)

    # set the origin to 0,0
    df.x -= X_BUMP_OFFSET
    df.y -= Y_BUMP_OFFSET

    # Flip it about Y axix
    df.x = df.x * -1

    # Re center about 0,0
    df.x += abs(df.x.min())

    # Offset to move into the ball area
    df.y = df.y + Y_OFFSET
    df.x = df.x + X_OFFSET

    odf = df[["Chip Ball Name", "x", "y"]].copy()
    odf.loc[:, "TYPE"] = "BUMP"
    return odf


def ball_map(input_filename, sheet_name, output_filename, loglevel):
    """ballco

    Args:
       input_filename:
       output_filename:
       sheet_name:
       output_filename:
       loglevel: int
    """
    COL_NAMES = [i for i in range(1, 17)]
    ROW_NAMES = [chr(i) for i in range(ord("A"), ord("U"))]
    EXCLUDE_NAMES = ("I", "O", "Q", "S")
    ROW_NAMES = [e for e in ROW_NAMES if e not in EXCLUDE_NAMES]
    if output_filename is None:
        output_filename = input_filename
    df = pd.DataFrame()
    try:
        df = pd.read_excel(
            input_filename,
            sheet_name=sheet_name,
            usecols="C:R",
            skiprows=[0],
            nrows=16,
        )
        df.columns = COL_NAMES
        df.index = ROW_NAMES
        df.fillna("", inplace=True)
    except Exception as e:  # noqa: F841
        click.echo(
            click.style(f"{str(e)} Error on processing {input_filename}", fg="red")
        )
        exit(1)
    y_ord = dict(zip(df.index, [i for i in range(len(df.index) - 1, -1, -1)]))
    flat = df.stack().to_frame()
    flat["Row"] = pd.Series([i[0] for i in flat.index.to_list()], index=flat.index)
    flat["Col"] = pd.Series([i[1] for i in flat.index.to_list()], index=flat.index)

    def f(x):
        return y_ord[x]

    flat["RowOrd"] = flat["Row"].apply(f)
    flat["ColOrd"] = flat["Col"] - 1
    flat["y"] = flat["RowOrd"] * PITCH  # + Y_OFFSET
    flat["x"] = flat["ColOrd"] * PITCH  # + X_OFFSET
    flat.rename(columns={0: "Chip Ball Name"}, inplace=True)
    odf = flat[["Chip Ball Name", "x", "y"]].copy()
    odf.loc[:, ["TYPE"]] = "BALL"
    return odf


# def ball_list(input_filename, sheet_name,
#            output_filename, loglevel):
#     """bump_map
#
#      Args:
#         input_filename:
#         output_filename:
#         sheet_name:
#         output_filename:
#         loglevel: int
#     """
#     pitch = 65000
#     if output_filename is None:
#         output_filename = input_filename
#     print(input_filename, output_filename)
#     df = pd.DataFrame()
#     try:
#         df = pd.read_excel(input_filename,
#                            sheet_name=sheet_name,
#                            skiprows=4
#                             )
#     except Exception as e:
#         click.echo(
#             click.style(
#                 "{} Error on processing {}".format(str(e), input_filename),
#                 fg="red"
#             )
#         )
#         exit(1)
#     # row_col = df['Ball Ref'].str.extract(r"([A-Z])([1-9][0-9]?$)").set_axis(
#     #     ['row_char', 'x'], axis=1).astype({'row_char': str, 'x': int})
#     # row_col['x'] -= 1
#     # row_col['y'] = row_col['row_char'].apply(ord).astype(int)
#     # f = lambda x: x - 66 if (x > 79) else x - 65
#     # row_col['y'] = row_col['y'].apply(f)
#     # co_ords = row_col.drop(['row_char'], axis=1)
#     # co_ords = co_ords*pitch
#     # co_ords['y'] = co_ords['y']*-1
#     # co_ords['y'] = co_ords['y'] + co_ords['y'].min().tolist() * -1
#
#     odf = pd.concat([df[['Ball Ref', 'Net Name', 'Counter']], co_ords], axis=1)
#     plt.scatter(odf.x, odf.y)
#     for index, row in odf.iterrows():
#         plt.annotate(row['Ball Ref'], (row.x, row.y + 300))
#
#     plt.show()
#     odf.to_excel(output_filename)
