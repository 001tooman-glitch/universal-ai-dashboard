import pandas as pd
import plotly.express as px


def build_top_chart(
    df,
    category_column,
    value_column,
    top_n=20
):

    chart_df = (
        df.groupby(category_column)[value_column]
        .sum()
        .reset_index()
        .sort_values(
            value_column,
            ascending=False
        )
        .head(top_n)
    )

    fig = px.bar(
        chart_df,
        x=value_column,
        y=category_column,
        orientation="h",
        title=f"ТОП {top_n}"
    )

    return fig


def build_abc_chart(
    abc_df
):

    summary = (
        abc_df.groupby("ABC")
        .size()
        .reset_index(name="Количество")
    )

    fig = px.bar(
        summary,
        x="ABC",
        y="Количество",
        color="ABC",
        title="ABC-анализ"
    )

    return fig


def build_xyz_chart(
    xyz_df
):

    summary = (
        xyz_df.groupby("XYZ")
        .size()
        .reset_index(name="Количество")
    )

    fig = px.bar(
        summary,
        x="XYZ",
        y="Количество",
        color="XYZ",
        title="XYZ-анализ"
    )

    return fig


def build_abc_xyz_heatmap(
    matrix_df
):

    heatmap = (
        matrix_df.groupby(
            ["ABC", "XYZ"]
        )
        .size()
        .reset_index(name="Количество")
    )

    pivot = heatmap.pivot(
        index="ABC",
        columns="XYZ",
        values="Количество"
    ).fillna(0)

    fig = px.imshow(
        pivot,
        text_auto=True,
        aspect="auto",
        title="Матрица ABC/XYZ"
    )

    return fig


def build_time_series_chart(
    trend_df,
    period_column,
    value_column
):

    fig = px.line(
        trend_df,
        x=period_column,
        y=value_column,
        markers=True,
        title=f"Динамика: {value_column}"
    )

    return fig


def build_pareto_chart(
    abc_df,
    item_column,
    value_column,
    top_n=30
):

    work_df = (
        abc_df.sort_values(
            value_column,
            ascending=False
        )
        .head(top_n)
    )

    work_df = work_df.copy()

    total = work_df[
        value_column
    ].sum()

    if total > 0:

        work_df["Накопленная доля"] = (
            work_df[value_column]
            .cumsum()
            / total
            * 100
        )

    else:

        work_df["Накопленная доля"] = 0

    fig = px.bar(
        work_df,
        x=item_column,
        y=value_column,
        title="Диаграмма Парето"
    )

    return fig


def build_kpi_cards(
    df,
    semantic_model
):

    result = {}

    measures = semantic_model.get(
        "measures",
        []
    )

    for measure in measures:

        try:

            value = pd.to_numeric(
                df[measure],
                errors="coerce"
            ).sum()

            result[measure] = value

        except Exception:

            pass

    result["rows"] = len(df)

    return result
