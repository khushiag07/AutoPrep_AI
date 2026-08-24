import pandas as pd
import numpy as np


class DataValidator:

    def __init__(self, original_df, cleaned_df):

        self.original_df = original_df.copy()
        self.cleaned_df = cleaned_df.copy()

        self.checks = []

    # --------------------------------------------------
    # MISSING VALUES
    # --------------------------------------------------

    def validate_missing_values(self):

        before = int(
            self.original_df.isna().sum().sum()
        )

        after = int(
            self.cleaned_df.isna().sum().sum()
        )

        passed = after <= before

        self.checks.append({
            "check": "Missing Values",
            "before": before,
            "after": after,
            "status": "PASS" if passed else "FAIL"
        })

    # --------------------------------------------------
    # DUPLICATES
    # --------------------------------------------------

    def validate_duplicates(self):

        before = int(
            self.original_df.duplicated().sum()
        )

        after = int(
            self.cleaned_df.duplicated().sum()
        )

        passed = after <= before

        self.checks.append({
            "check": "Duplicate Rows",
            "before": before,
            "after": after,
            "status": "PASS" if passed else "FAIL"
        })

    # --------------------------------------------------
    # ROW COUNT
    # --------------------------------------------------

    def validate_row_count(self):

        before = len(self.original_df)

        after = len(self.cleaned_df)

        passed = after <= before

        self.checks.append({
            "check": "Row Count",
            "before": before,
            "after": after,
            "status": "PASS" if passed else "FAIL"
        })

    # --------------------------------------------------
    # COLUMN COUNT
    # --------------------------------------------------

    def validate_column_count(self):

        before = len(self.original_df.columns)

        after = len(self.cleaned_df.columns)

        passed = before == after

        self.checks.append({
            "check": "Column Count",
            "before": before,
            "after": after,
            "status": "PASS" if passed else "FAIL"
        })

    # --------------------------------------------------
    # COLUMN PRESERVATION
    # --------------------------------------------------

    def validate_columns(self):

        original_columns = set(
            self.original_df.columns
        )

        cleaned_columns = set(
            self.cleaned_df.columns
        )

        missing_columns = list(
            original_columns - cleaned_columns
        )

        new_columns = list(
            cleaned_columns - original_columns
        )

        passed = len(missing_columns) == 0

        self.checks.append({
            "check": "Column Preservation",
            "missing_columns": missing_columns,
            "new_columns": new_columns,
            "status": "PASS" if passed else "FAIL"
        })

    # --------------------------------------------------
    # DATA TYPES
    # --------------------------------------------------

    def validate_data_types(self):

        type_changes = []

        for column in self.original_df.columns:

            if column not in self.cleaned_df.columns:
                continue

            before_type = str(
                self.original_df[column].dtype
            )

            after_type = str(
                self.cleaned_df[column].dtype
            )

            if before_type != after_type:

                type_changes.append({
                    "column": column,
                    "before": before_type,
                    "after": after_type
                })

        self.checks.append({
            "check": "Data Types",
            "changes": type_changes,
            "status": "PASS"
        })

    # --------------------------------------------------
    # CONSTANT COLUMNS
    # --------------------------------------------------

    def validate_constant_columns(self):

        constant_columns = []

        for column in self.cleaned_df.columns:

            if self.cleaned_df[column].nunique(
                dropna=False
            ) <= 1:

                constant_columns.append(column)

        self.checks.append({
            "check": "Constant Columns",
            "columns": constant_columns,
            "count": len(constant_columns),
            "status": "PASS"
        })

    # --------------------------------------------------
    # NUMERICAL VALIDITY
    # --------------------------------------------------

    def validate_numeric_values(self):

        invalid_values = []

        numerical_columns = (
            self.cleaned_df
            .select_dtypes(include=np.number)
            .columns
        )

        for column in numerical_columns:

            values = self.cleaned_df[column]

            invalid_count = int(
                (~np.isfinite(values)).sum()
            )

            if invalid_count > 0:

                invalid_values.append({
                    "column": column,
                    "invalid_values": invalid_count
                })

        passed = len(invalid_values) == 0

        self.checks.append({
            "check": "Numerical Validity",
            "invalid_columns": invalid_values,
            "status": "PASS" if passed else "FAIL"
        })

    # --------------------------------------------------
    # RUN ALL VALIDATIONS
    # --------------------------------------------------

    def validate(self):

        self.checks = []

        self.validate_missing_values()

        self.validate_duplicates()

        self.validate_row_count()

        self.validate_column_count()

        self.validate_columns()

        self.validate_data_types()

        self.validate_constant_columns()

        self.validate_numeric_values()

        passed = sum(
            check["status"] == "PASS"
            for check in self.checks
        )

        total = len(self.checks)

        score = round(
            (passed / total) * 100
        )

        return {

            "validation_score": score,

            "status": (
                "PASSED"
                if score >= 80
                else "NEEDS_REVIEW"
            ),

            "checks": self.checks
        }