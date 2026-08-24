import pandas as pd
import numpy as np


class DataProfiler:

    def __init__(self, df: pd.DataFrame):
        self.df = df


    def profile(self):

        df = self.df

        return {
            "dataset": self.dataset_summary(df),
            "columns": self.column_profile(df),
            "quality": self.quality_summary(df),
            "outliers": self.detect_outliers(df)
        }


    # ==========================================
    # DATASET SUMMARY
    # ==========================================

    def dataset_summary(self, df):

        return {
            "rows": int(df.shape[0]),

            "columns": int(df.shape[1]),

            "memory_usage_mb": round(
                df.memory_usage(
                    deep=True
                ).sum()
                / (1024 * 1024),
                2
            )
        }


    # ==========================================
    # COLUMN PROFILE
    # ==========================================

    def column_profile(self, df):

        columns = []

        for column in df.columns:

            series = df[column]

            columns.append({

                "name": column,

                "dtype": str(
                    series.dtype
                ),

                "missing": int(
                    series.isna().sum()
                ),

                "missing_percentage": round(
                    series.isna().mean() * 100,
                    2
                ),

                "unique": int(
                    series.nunique()
                ),

                "unique_percentage": round(
                    series.nunique()
                    / len(df) * 100,
                    2
                )
            })

        return columns


    # ==========================================
    # DATA QUALITY
    # ==========================================

    def quality_summary(self, df):

        total_cells = (
            df.shape[0] *
            df.shape[1]
        )

        missing_cells = int(
            df.isna().sum().sum()
        )

        duplicate_rows = int(
            df.duplicated().sum()
        )


        missing_percentage = 0

        if total_cells > 0:

            missing_percentage = round(
                missing_cells /
                total_cells * 100,
                2
            )


        duplicate_percentage = 0

        if len(df) > 0:

            duplicate_percentage = round(
                duplicate_rows /
                len(df) * 100,
                2
            )


        return {

            "missing_cells":
                missing_cells,

            "missing_percentage":
                missing_percentage,

            "duplicate_rows":
                duplicate_rows,

            "duplicate_percentage":
                duplicate_percentage
        }


    # ==========================================
    # OUTLIER DETECTION
    # ==========================================

    def detect_outliers(self, df):

        outliers = []


        numeric_columns = df.select_dtypes(
            include=np.number
        ).columns


        for column in numeric_columns:

            series = df[column].dropna()


            # Not enough data
            if len(series) < 4:
                continue


            q1 = series.quantile(0.25)

            q3 = series.quantile(0.75)

            iqr = q3 - q1


            # No variation
            if iqr == 0:
                continue


            lower_bound = (
                q1 - 1.5 * iqr
            )

            upper_bound = (
                q3 + 1.5 * iqr
            )


            mask = (
                (series < lower_bound)
                |
                (series > upper_bound)
            )


            count = int(
                mask.sum()
            )


            if count > 0:

                outliers.append({

                    "column": column,

                    "count": count,

                    "percentage": round(
                        count /
                        len(series) * 100,
                        2
                    ),

                    "lower_bound": round(
                        float(lower_bound),
                        3
                    ),

                    "upper_bound": round(
                        float(upper_bound),
                        3
                    )
                })


        return outliers