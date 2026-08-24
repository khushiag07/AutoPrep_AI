import pandas as pd
import numpy as np


class CleaningEngine:
    def __init__(
        self,
        df: pd.DataFrame,
        recommendations=None
    ):

        self.df = df.copy()

        self.recommendations = (
            recommendations or []
        )

        self.audit_log = []

    def get_recommendations(self, action):

        return [
            r for r in self.recommendations
            if r.get("action") == action
        ]


    # --------------------------------------------------
    # DUPLICATES
    # --------------------------------------------------

    def remove_duplicates(self):

        before = len(self.df)

        self.df = self.df.drop_duplicates()

        removed = before - len(self.df)

        self.audit_log.append({
            "operation": "remove_duplicates",
            "rows_removed": removed
        })

    # --------------------------------------------------
    # MISSING VALUES
    # --------------------------------------------------

    def handle_missing_values(self):

        numerical_columns = self.df.select_dtypes(
            include=np.number
        ).columns

        categorical_columns = self.df.select_dtypes(
            include=["object", "category", "bool"]
        ).columns

        # Numerical → median
        for column in numerical_columns:

            missing = int(self.df[column].isna().sum())

            if missing > 0:

                median_value = self.df[column].median()

                self.df[column] = self.df[column].fillna(
                    median_value
                )

                self.audit_log.append({
                    "operation": "missing_value_imputation",
                    "column": column,
                    "strategy": "median",
                    "values_filled": missing
                })

        # Categorical → mode
        for column in categorical_columns:

            missing = int(self.df[column].isna().sum())

            if missing > 0:

                mode_values = self.df[column].mode()

                if len(mode_values) > 0:

                    mode_value = mode_values.iloc[0]

                    self.df[column] = self.df[column].fillna(
                        mode_value
                    )

                    self.audit_log.append({
                        "operation": "missing_value_imputation",
                        "column": column,
                        "strategy": "mode",
                        "values_filled": missing
                    })

    # --------------------------------------------------
    # CATEGORICAL NORMALIZATION
    # --------------------------------------------------

    def normalize_categories(self):

        categorical_columns = self.df.select_dtypes(
            include=["object", "category"]
        ).columns

        for column in categorical_columns:

            before = self.df[column].copy()

            self.df[column] = (
                self.df[column]
                .astype(str)
                .str.strip()
                .str.lower()
            )

            changed = int(
                (before.astype(str) != self.df[column])
                .sum()
            )

            if changed > 0:

                self.audit_log.append({
                    "operation": "category_normalization",
                    "column": column,
                    "rows_changed": changed
                })

    # --------------------------------------------------
    # OUTLIER CAPPING
    # --------------------------------------------------

    def cap_outliers(self):

        numerical_columns = self.df.select_dtypes(
            include=np.number
        ).columns

        for column in numerical_columns:

            series = self.df[column]

            q1 = series.quantile(0.25)
            q3 = series.quantile(0.75)

            iqr = q3 - q1

            if iqr == 0:
                continue

            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr

            outliers = (
                (series < lower_bound) |
                (series > upper_bound)
            )

            count = int(outliers.sum())

            if count > 0:

                self.df[column] = self.df[column].clip(
                    lower=lower_bound,
                    upper=upper_bound
                )

                self.audit_log.append({
                    "operation": "outlier_capping",
                    "column": column,
                    "outliers_modified": count,
                    "lower_bound": lower_bound,
                    "upper_bound": upper_bound
                })

    # --------------------------------------------------
    # COMPLETE CLEANING PIPELINE
    # --------------------------------------------------

    def clean(self):

    # ------------------------------------------
    # DUPLICATES
    # ------------------------------------------

        duplicate_recommendations = (
            self.get_recommendations(
                "remove_duplicates"
            )
        )

        if duplicate_recommendations:

            self.remove_duplicates()


        # ------------------------------------------
        # MISSING VALUES
        # ------------------------------------------

        missing_recommendations = (
            self.get_recommendations(
                "impute"
            )
        )

        if missing_recommendations:

            self.handle_missing_values()


        # ------------------------------------------
        # CATEGORY NORMALIZATION
        # ------------------------------------------

        category_recommendations = (
            self.get_recommendations(
                "normalize_categories"
            )
        )

        if category_recommendations:

            self.normalize_categories()


        # ------------------------------------------
        # OUTLIERS
        # ------------------------------------------

        # IMPORTANT:
        # We deliberately do NOT automatically
        # cap outliers.

        outlier_recommendations = (
            self.get_recommendations(
                "review_outliers"
            )
        )

        for recommendation in outlier_recommendations:

            self.audit_log.append({

                "operation":
                    "outlier_review_required",

                "column":
                    recommendation.get("column"),

                "message":
                    "Potential outliers detected. "
                    "No automatic modification applied."
            })


        return self.df, self.audit_log