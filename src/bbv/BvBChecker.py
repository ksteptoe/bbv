from collections import Counter

import pandas as pd

from bbv import __version__


class BvBCHeck(object):
    def __init__(self, balls: pd.DataFrame, bumps: pd.DataFrame, data_set):
        self.data_set = data_set
        # Objects
        self.balls = list(balls["Chip Ball Name"])
        self.bumps = list(bumps["Chip Ball Name"])
        # Count of objects
        self.num_balls = len(self.balls)
        self.num_bumps = len(self.bumps)
        # Unique Objects
        self.unique_balls = set(self.balls)
        self.unique_bumps = set(self.bumps)
        # Count of unique objects
        self.num_unique_balls = len(self.unique_balls)
        self.num_unique_bumps = len(self.unique_bumps)
        # Count  of unique objects
        self.unique_balls_counter = Counter(self.balls)
        self.unique_balls_counter_ordered = {
            k: v
            for k, v in sorted(
                self.unique_balls_counter.items(), key=lambda item: item[1]
            )
        }
        self.unique_bump_counter = Counter(self.bumps)
        # Diff of objects
        self.bump_diff = self.unique_balls - self.unique_bumps
        self.ball_diff = self.unique_bumps - self.unique_balls
        self.sym_diff = self.unique_balls ^ self.unique_bumps

        # self.filtered_diff = {i for i in self.diff if not i.startswith('(internal')}
        pass

    def __repr__(self):
        return f"BvBCHeck ({self.num_unique_bumps},{self.num_unique_balls})"

    def print_line(self):
        print(60 * "-")

    def section_break(self):
        print(2 * "\n")

    def print_ball_count(self, dct):
        print("Num Ball Name")
        for ball, number in dct.items():
            if number > 1:
                print(f" {number} x {ball}")

    def print_sym_diff(self, diffs):
        self.print_line()
        for diff in diffs:
            print(diff)

    def report(self):
        print("Program Version")
        self.print_line()
        print(f"BumpvBall Checker Version: {__version__}\n")
        self.section_break()

        print("Input Files Used:")
        self.print_line()
        print(f'PCS_Filename: "{self.data_set.pcs_filename}"')
        print(f'PCS_SheetName: "{self.data_set.pcs_sheetname}"')
        print(f"PCS_RowOffset: {self.data_set.pcs_rowoffset}")
        print(f'Sondrel_Filename: "{self.data_set.sondrel_filename}"')
        print(f'Sondrel_SheetName: "{self.data_set.sondrel_sheetname}"')
        print(f"Sondrel_RowOffset: {self.data_set.sondrel_rowoffset}\n")
        self.section_break()
        print("Bump and Ball Counts")
        self.print_line()
        print(f"Number of bumps: {self.num_bumps}")
        print(f"Number of balls: {self.num_balls}\n")
        print(f"Number of unique bumps: {self.num_bumps}")
        print(f"Number of unique balls: {self.num_unique_balls}\n")
        self.section_break()
        print("Differances")
        self.print_line()
        bump_diff_filtered = {
            i for i in self.bump_diff if not i.startswith("(internal")
        }
        print(
            f"Ball Names found in bumps not in balls ( internal signals filtered):\n "
            f"{bump_diff_filtered}\n"
        )
        print(f"Ball Names found in balls not in bumps :\n {self.ball_diff}\n")
        print("Symmetric Difference of balls and bumps ie nets NOT common to both:")
        self.print_sym_diff(self.sym_diff)
        self.section_break()

        print("Ball count with signals > 1")
        self.print_line()
        self.print_ball_count(self.unique_balls_counter_ordered)
        print()
        self.print_line()
