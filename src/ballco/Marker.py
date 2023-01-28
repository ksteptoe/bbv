import pandas as pd


class Marker(object):
    def __init__(
        self,
        name: str,
        ident: str,
        x_min: int,
        y_min: int,
        x_max: int,
        y_max: int,
        x_offset: int = 0,
        y_offset: int = 0,
    ):
        self.name = name
        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max
        self.marker = pd.DataFrame(
            {
                "Chip Ball Name": self.label(ident),
                "x": [x_min, x_max, x_min, x_max],
                "y": [y_min, y_max, y_max, y_min],
            }
        )
        self.marker.x += x_offset
        self.marker.y += y_offset
        # Todo add two other marker co-ords

    def __repr__(self):
        return f"{self.marker}"

    def offset(self, x_offset, y_offset):
        self.marker.x += x_offset
        self.marker.y += y_offset

    @staticmethod
    def label(ident: str):
        return [ident + "_LL", ident + "_UR", ident + "_UL", ident + "_LR"]
