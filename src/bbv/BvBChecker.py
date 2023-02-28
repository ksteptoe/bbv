from collections import Counter
from datetime import datetime

import pandas as pd

from bbv import __version__

FILTER_LIST = ("(internal", "none")


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
        self.bump_diff = self.unique_bumps - self.unique_balls
        self.ball_diff = self.unique_balls - self.unique_bumps
        self.sym_diff = self.unique_balls ^ self.unique_bumps
        pass

    def __repr__(self):
        return f"BvBCHeck ({self.num_unique_bumps},{self.num_unique_balls})"

    def filter(self, filter_obj, filter_list):
        filtered_obj = filter_obj
        filtered = set()
        for f in filter_list:
            filter_set = {i for i in filter_obj if i.startswith(f)}
            filtered_obj -= filter_set
            filtered = filtered | filter_set
        return (filtered_obj, filtered)

    def print_line(self):
        print(60 * "-")

    def section_break(self):
        print(2 * "\n")

    def print_ball_count(self, dct):
        print("Num Ball Name")
        for ball, number in dct.items():
            if number > 1:
                print(f" {number} x {ball}")

    # def print_sym_diff(self, diffs):
    #     self.print_line()
    #     for diff in diffs:
    #         print(diff)

    def report(self):
        print(f"bbv version: {__version__}")
        print(f"{datetime.today().strftime('%d/%m/%Y')}")
        print(
            f'PCS_Filename: "{self.data_set.pcs_filename}" '
            f'PCS_SheetName: "{self.data_set.pcs_sheetname}" '
            f"PCS_RowOffset: {self.data_set.pcs_rowoffset}"
        )
        print(
            f'Sondrel_Filename: "{self.data_set.sondrel_filename}" '
            f'Sondrel_SheetName: "{self.data_set.sondrel_sheetname}" '
            f"Sondrel_RowOffset: {self.data_set.sondrel_rowoffset}\n"
        )
        print(f"Number of bumps: {self.num_bumps}")
        print(f"Number of balls: {self.num_balls}\n")
        print(f"Number of unique bumps: {self.num_bumps}")
        print(f"Number of unique balls: {self.num_unique_balls}\n")
        self.section_break()
        print("Differences")
        self.print_line()
        bump_diff_filtered, filtered = self.filter(self.bump_diff, FILTER_LIST)
        print(
            f"Ball Names found in bumps not in balls ( internal signals filtered):\n "
            f"{bump_diff_filtered}\n"
        )
        print("\nNames of items filtered in the process:")
        for f in filtered:
            print(f)
        print("\n")
        print(f"Ball Names found in balls not in bumps :\n {self.ball_diff}\n")
        print(
            "Symmetric Difference of balls and bumps ie nets NOT common to "
            "both with filtering on:"
        )
        sym_diff_filtered, filtered = self.filter(self.sym_diff, FILTER_LIST)
        print(sym_diff_filtered)
        print("\nNames of items filtered in the process:")
        for f in filtered:
            print(f)
        print("\n")

        # print("Ball count with signals > 1")
        # self.print_line()
        # self.print_ball_count(self.unique_balls_counter_ordered)
        # print()
        # self.print_line()
