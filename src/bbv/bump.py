import click
import pandas as pd

from bbv.globals import X_BUMP_OFFSET, X_OFFSET, Y_BUMP_OFFSET, Y_OFFSET


def bump_map(input_filename, sheet_name, skiprows):
    """bump_map

    Args:
       input_filename:
       sheet_name:
       skiprows: int
    """

    df = pd.DataFrame()
    try:
        df = pd.read_excel(input_filename, sheet_name=sheet_name, skiprows=skiprows)
    except Exception as e:  # noqa: F841
        click.echo(
            click.style(f"{str(e)} Error on processing {input_filename}", fg="red")
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
