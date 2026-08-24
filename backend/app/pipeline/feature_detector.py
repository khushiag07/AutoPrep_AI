class FeatureDetector:

    def __init__(self, df):

        self.df = df

    def constant_columns(self):

        results = []

        for column in self.df.columns:

            unique_count = (
                self.df[column]
                .nunique(dropna=False)
            )

            if unique_count <= 1:

                results.append(column)

        return results

    def low_variance_columns(
        self,
        threshold=0.01
    ):

        results = []

        numerical_columns = (
            self.df
            .select_dtypes(include="number")
            .columns
        )

        for column in numerical_columns:

            variance = self.df[column].var()

            if variance <= threshold:

                results.append({
                    "column": column,
                    "variance": variance
                })

        return results