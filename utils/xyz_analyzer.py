import pandas as pd


def run_xyz_analysis(
    df,
    item_column,
    value_column
):

    work_df = df.copy()

    work_df[value_column] = pd.to_numeric(
        work_df[value_column],
        errors="coerce"
    )

    xyz = (
        work_df.groupby(item_column)[value_column]
        .agg([
            "mean",
            "std"
        ])
        .reset_index()
    )

    xyz["std"] = xyz["std"].fillna(0)

    xyz["CV"] = (
        xyz["std"]
        / xyz["mean"].replace(0, 1)
    )

    def classify(cv):

        if cv <= 0.10:
            return "X"

        if cv <= 0.25:
            return "Y"

        return "Z"

    xyz["XYZ"] = xyz["CV"].apply(
        classify
    )

    xyz = xyz.sort_values(
        "CV"
    )

    xyz = xyz.rename(
        columns={
            "mean": "Среднее",
            "std": "Стандартное отклонение",
            "CV": "Коэффициент вариации"
        }
    )

    return xyz
