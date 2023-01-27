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

    def plot(self, expr):
        if self.state:
            disp = self.df
            if self.type != "MARKER":
                disp = self.df[self.df["Chip Ball Name"].str.match(expr)]
                for index, row in disp.iterrows():
                    plt.annotate(
                        row[0], (row.x, row.y + self.offset), fontsize=5, rotation=30
                    )
            if self.type == "MARKER":
                self.size = 3
                plt.scatter(disp.x, disp.y, s=self.size)
            else:
                plt.scatter(disp.x, disp.y, s=20)

    # x = [-1, 0.5, 1, -0.5]
    # y = [0.5, 1, -0.5, -1]
    #
    # plt.plot(x, y, 'ro')
    #
    # def connectpoints(x, y, p1, p2):
    #     x1, x2 = x[p1], x[p2]
    #     y1, y2 = y[p1], y[p2]
    #     plt.plot([x1, x2], [y1, y2], 'k-')
    #
    # connectpoints(x, y, 0, 1)
    # connectpoints(x, y, 2, 3)
    #
    # plt.axis('equal')
    # plt.show()
    #

    def show(self):
        if self.state:
            plt.show()
