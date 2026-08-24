import pandas as pd


class DataIntelligence:

    def analyze(self, profile, df):

        recommendations = []

        # ==========================================
        # COLUMN ANALYSIS
        # ==========================================

        for column in profile["columns"]:

            name = column["name"]
            dtype = column["dtype"]

            missing = column["missing"]
            missing_pct = column["missing_percentage"]

            unique = column["unique"]
            unique_pct = column["unique_percentage"]

            series = df[name]

            # --------------------------------------
            # MISSING VALUES
            # --------------------------------------

            if missing > 0:

                if missing_pct >= 50:

                    recommendations.append({
                        "column": name,
                        "issue": "High missing values",
                        "severity": "high",
                        "action": "review_or_drop",
                        "reason":
                            f"{missing_pct}% of values "
                            "are missing."
                    })

                elif missing_pct >= 10:

                    recommendations.append({
                        "column": name,
                        "issue": "Moderate missing values",
                        "severity": "medium",
                        "action": "impute",
                        "reason":
                            f"{missing_pct}% of values "
                            "are missing."
                    })

                else:

                    recommendations.append({
                        "column": name,
                        "issue": "Missing values",
                        "severity": "low",
                        "action": "impute",
                        "reason":
                            f"Only {missing_pct}% of "
                            "values are missing."
                    })


            # --------------------------------------
            # CONSTANT COLUMN
            # --------------------------------------

            if unique <= 1:

                recommendations.append({
                    "column": name,
                    "issue": "Constant column",
                    "severity": "medium",
                    "action": "review",
                    "reason":
                        "This column contains only "
                        "one unique value and provides "
                        "little predictive information."
                })


            # --------------------------------------
            # NEAR CONSTANT
            # --------------------------------------

            elif len(df) > 0 and (
                unique_pct < 1
            ):

                recommendations.append({
                    "column": name,
                    "issue": "Near-constant column",
                    "severity": "low",
                    "action": "review",
                    "reason":
                        "Very few unique values exist "
                        "relative to the dataset size."
                })


            # --------------------------------------
            # POTENTIAL ID
            # --------------------------------------

            if unique_pct >= 95:

                recommendations.append({
                    "column": name,
                    "issue": "Potential identifier",
                    "severity": "medium",
                    "action": "review",
                    "reason":
                        "Almost every row contains a "
                        "unique value. This may be an "
                        "identifier column."
                })


            # --------------------------------------
            # CATEGORICAL ANALYSIS
            # --------------------------------------

            if (
                dtype == "object"
                or str(dtype).startswith("category")
            ):

                if unique > 20:

                    recommendations.append({
                        "column": name,
                        "issue": "High-cardinality category",
                        "severity": "medium",
                        "action": "review",
                        "reason":
                            f"{unique} unique categories "
                            "detected. Encoding may become "
                            "inefficient."
                    })


                # Category normalization
                values = (
                    series
                    .dropna()
                    .astype(str)
                    .str.strip()
                )

                normalized = (
                    values
                    .str.lower()
                )

                original_unique = values.nunique()
                normalized_unique = normalized.nunique()

                if normalized_unique < original_unique:

                    recommendations.append({
                        "column": name,
                        "issue":
                            "Category inconsistency",
                        "severity": "medium",
                        "action":
                            "normalize_categories",
                        "reason":
                            "Different capitalization or "
                            "spacing appears to represent "
                            "the same category."
                    })


            # --------------------------------------
            # NUMERICAL SKEWNESS
            # --------------------------------------

            if pd.api.types.is_numeric_dtype(series):

                clean_series = series.dropna()

                if len(clean_series) > 10:

                    skewness = clean_series.skew()

                    if abs(skewness) > 2:

                        recommendations.append({
                            "column": name,
                            "issue": "Highly skewed feature",
                            "severity": "medium",
                            "action": "transform",
                            "reason":
                                f"Skewness is "
                                f"{round(skewness, 2)}. "
                                "Consider a transformation "
                                "such as log or Yeo-Johnson."
                        })

                    elif abs(skewness) > 1:

                        recommendations.append({
                            "column": name,
                            "issue": "Moderately skewed feature",
                            "severity": "low",
                            "action": "review",
                            "reason":
                                f"Skewness is "
                                f"{round(skewness, 2)}."
                        })


        # ==========================================
        # DUPLICATES
        # ==========================================

        quality = profile["quality"]

        duplicate_rows = quality["duplicate_rows"]

        if duplicate_rows > 0:

            recommendations.append({
                "column": None,
                "issue": "Duplicate rows",
                "severity": "medium",
                "action": "remove_duplicates",
                "reason":
                    f"{duplicate_rows} duplicate rows "
                    "detected."
            })


        # ==========================================
        # OUTLIERS
        # ==========================================

        for outlier in profile["outliers"]:

            column = outlier["column"]
            percentage = outlier["percentage"]

            if percentage >= 10:
                severity = "high"

            elif percentage >= 5:
                severity = "medium"

            else:
                severity = "low"


            recommendations.append({

                "column": column,

                "issue": "Potential outliers",

                "severity": severity,

                "action": "review_outliers",

                "reason":
                    f"{outlier['count']} potential "
                    f"outliers detected "
                    f"({percentage}%). "
                    "Do not automatically delete them.",

                "lower_bound":
                    outlier["lower_bound"],

                "upper_bound":
                    outlier["upper_bound"]
            })


        # ==========================================
        # TARGET COLUMN DETECTION
        # ==========================================

        target_candidates = self.detect_target_candidates(
            df
        )


        # ==========================================
        # SUMMARY
        # ==========================================

        high = sum(
            1
            for r in recommendations
            if r["severity"] == "high"
        )

        medium = sum(
            1
            for r in recommendations
            if r["severity"] == "medium"
        )

        low = sum(
            1
            for r in recommendations
            if r["severity"] == "low"
        )


        return {

            "recommendations":
                recommendations,

            "target_candidates":
                target_candidates,

            "summary": {

                "total_issues":
                    len(recommendations),

                "high": high,

                "medium": medium,

                "low": low
            }
        }


    # ==========================================
    # TARGET DETECTION
    # ==========================================

    def detect_target_candidates(self, df):

        candidates = []

        target_names = [

            "target",
            "label",
            "class",
            "y",
            "outcome",
            "result",
            "prediction",
            "response",
            "churn",
            "default",
            "survived"

        ]


        for column in df.columns:

            name = column.lower().strip()


            # Name based detection

            if name in target_names:

                candidates.append({
                    "column": column,
                    "reason":
                        "Column name suggests it may "
                        "represent the prediction target.",
                    "confidence": "high"
                })

                continue


            # Low-cardinality categorical target

            unique = df[column].nunique()

            if (
                unique >= 2
                and unique <= 10
                and len(df) > 0
            ):

                candidates.append({
                    "column": column,
                    "reason":
                        "Column has low cardinality "
                        "and may represent a target.",
                    "confidence": "low"
                })


        return candidates