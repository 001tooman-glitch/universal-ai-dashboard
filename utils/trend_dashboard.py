import pandas as pd
import plotly.express as px


def build_trend_chart(
    df,
    semantic_model
):
    """
    Построение графика динамики
    по главному показателю.
    """

    entities = semantic_model.get(
        "entities",
        {}
    )

    if "date" not in entities:

        return None

    if "amount" not in entities:

        return None

    try:

        date_column = (
            entities["date"][0]
        )

        amount_column = (
            entities["amount"][0]
        )

        trend_df = (
            df.groupby(date_column)[amount_column]
            .sum()
            .reset_index()
        )

        fig = px.line(
            trend_df,
            x=date_column,
            y=amount_column,
            markers=True,
            title="📈 Динамика стоимости по периодам"
        )

        fig.update_layout(
            height=500
        )

        return fig

    except Exception:

        return None
