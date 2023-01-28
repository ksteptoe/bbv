import matplotlib.pylab as plt
import pandas as pd


class Disp(object):
    def __init__(self, name: str, type: str, df: pd.DataFrame, offset: int):
        self.name = name
        self.type = type
        self.df = df
        self.offset = offset
        self.state = True
        self.size = 100

    def __repr__(self):
        return f"{self.type} {self.df}"

    def toggle_state(self):
        self.state = not self.state

    def status(self):
        print(f"{self.name} {self.state}")

    @staticmethod
    def connect_points(x, y):
        plt.plot(x, y, "+k-", linewidth=0.25)

    @staticmethod
    def order_points(disp):
        x_min = disp.x.min()
        x_max = disp.x.max()
        y_min = disp.y.min()
        y_max = disp.y.max()
        x = [x_min, x_max, x_max, x_min, x_min]
        y = [y_min, y_min, y_max, y_max, y_min]
        return (x, y)

    def marker(self, disp):
        # self.size = 3
        # plt.scatter(disp.x, disp.y, s=self.size)
        ordered = self.order_points(disp)
        self.connect_points(ordered[0], ordered[1])

    def plot(self, expr):
        disp = self.df
        if self.state:
            if self.type == "MARKER":
                self.marker(disp)
            else:
                disp = self.df[self.df["Chip Ball Name"].str.match(expr)]
                for index, row in disp.iterrows():
                    plt.annotate(
                        row[0], (row.x, row.y + self.offset), fontsize=10, rotation=30
                    )
                plt.scatter(disp.x, disp.y, s=20)

    def show(self):
        if self.state:
            plt.show()
