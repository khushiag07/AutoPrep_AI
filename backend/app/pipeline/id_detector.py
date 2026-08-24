import pandas as pd


class IDDetector:

    ID_KEYWORDS = [
        "id",
        "uuid",
        "identifier",
        "customer_id",
        "user_id",
        "employee_id",
        "transaction_id"
    ]

    def __init__(self, df):

        self.df = df

    def detect(self):

        results = []

        for column in self.df.columns:

            name = column.lower()

            unique_ratio = (
                self.df[column]
                .nunique(dropna=True)
                / len(self.df)
            )

            keyword_match = any(
                keyword in name
                for keyword in self.ID_KEYWORDS
            )

            if (
                keyword_match
                and unique_ratio > 0.8
            ):

                results.append({

                    "column": column,

                    "unique_ratio":
                        round(unique_ratio, 3),

                    "reason":
                        "Likely identifier column"
                })

        return results