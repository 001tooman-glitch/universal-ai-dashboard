import pandas as pd


def run_abc_analysis(
    df,
    item_column,
    value_column
):

    abc = (
        df.groupby(item_column)[value_column]
        .sum()
        .reset_index()
        .sort_values(
            value_column,
            ascending=False
        )
    )

    total = abc[value_column].sum()

    if total == 0:
        abc["Доля"] = 0
        abc["Накопленная доля"] = 0
        abc["ABC"] = "C"
        return abc

    abc["Доля"] = (
        abc[value_column] / total
    )

    abc["Накопленная доля"] = (
        abc["Доля"].cumsum()
    )

    def classify(value):

        if value <= 0.80:
            return "A"

        if value <= 0.95:
            return "B"

        return "C"

    abc["ABC"] = (
        abc["Накопленная доля"]
        .apply(classify)
    )

    return abc
