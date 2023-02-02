import click
import pandas as pd

from bbv.globals import PITCH


def ball_map(input_filename, sheet_name, output_filename, loglevel):
    """ball_map

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
    flat["y"] = flat["RowOrd"] * PITCH
    flat["x"] = flat["ColOrd"] * PITCH
    flat.rename(columns={0: "Chip Ball Name"}, inplace=True)
    odf = flat[["Chip Ball Name", "x", "y"]].copy()
    odf.loc[:, ["TYPE"]] = "BALL"
    return odf
