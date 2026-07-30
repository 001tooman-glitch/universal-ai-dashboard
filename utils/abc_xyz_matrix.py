import pandas as pd


def build_abc_xyz_matrix(
    abc_df,
    xyz_df,
    item_column
):

    matrix = pd.merge(
        abc_df[
            [
                item_column,
                "ABC"
            ]
        ],
        xyz_df[
            [
                item_column,
                "XYZ"
            ]
        ],
        on=item_column,
        how="inner"
    )

    matrix["ABC_XYZ"] = (
        matrix["ABC"]
        + matrix["XYZ"]
    )

    summary = (
        matrix.groupby("ABC_XYZ")
        .size()
        .reset_index(name="Количество")
        .sort_values("ABC_XYZ")
    )

    return matrix, summary
