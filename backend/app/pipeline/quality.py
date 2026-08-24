import pandas as pd
import numpy as np


class DataQualityAnalyzer:

    def __init__(self, df):

        self.df = df

    # ---------------------------------------------
    # Missing score
    # ---------------------------------------------

    def missing_score(self):

        total_cells = (
            self.df.shape[0] *
            self.df.shape[1]
        )

        if total_cells == 0:
            return 100

        missing_cells = int(
            self.df.isna().sum().sum()
        )

        missing_percentage = (
            missing_cells /
            total_cells
        ) * 100

        return round(
            max(0, 100 - missing_percentage),
            2
        )

    # ---------------------------------------------
    # Duplicate score
    # ---------------------------------------------

    def duplicate_score(self):

        if len(self.df) == 0:
            return 100

        duplicates = (
            self.df.duplicated().sum()
        )

        duplicate_percentage = (
            duplicates /
            len(self.df)
        ) * 100

        return round(
            max(0, 100 - duplicate_percentage),
            2
        )

    # ---------------------------------------------
    # Overall score
    # ---------------------------------------------

    def calculate_score(self):

        missing = self.missing_score()

        duplicate = self.duplicate_score()

        score = (
            missing * 0.6 +
            duplicate * 0.4
        )

        return round(score, 2)

    # ---------------------------------------------
    # Full report
    # ---------------------------------------------

    def generate_report(self):

        return {

            "missing_score":
                self.missing_score(),

            "duplicate_score":
                self.duplicate_score(),

            "overall_score":
                self.calculate_score()
        }