import pandas as pd


class Marker(object):
    def __init__(
        self,
        name: str,
        ident: str,
        df: pd.DataFrame,
        x_offset: int = 0,
        y_offset: int = 0,
        halo: int = 5,
    ):
        self.name = name
        self.x_min = df.x.min() - halo
        self.y_min = df.y.min() - halo
        self.x_max = df.x.max() + halo
        self.y_max = df.y.max() + halo
        self.marker = pd.DataFrame(
            {
                "Chip Ball Name": self.label(ident),
                "x": [self.x_min, self.x_max, self.x_min, self.x_max],
                "y": [self.y_min, self.y_max, self.y_max, self.y_min],
            }
        )
        self.marker.x += x_offset
        self.marker.y += y_offset

    def __repr__(self):
        return f"{self.marker}"

    def offset(self, x_offset, y_offset):
        self.marker.x += x_offset
        self.marker.y += y_offset

    @staticmethod
    def label(ident: str):
        return [ident + "_LL", ident + "_UR", ident + "_UL", ident + "_LR"]
