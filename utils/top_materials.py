import pandas as pd


def build_top_materials(
    df,
    product_column,
    amount_column,
    top_n=20
):

    result = (
        df.groupby(product_column)[amount_column]
        .sum()
        .reset_index()
        .sort_values(
            amount_column,
            ascending=False
        )
        .head(top_n)
    )

    return result
