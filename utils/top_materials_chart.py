import plotly.express as px


def build_top_materials_chart(
    top_df,
    product_column,
    amount_column
):

    fig = px.bar(
        top_df,
        x=amount_column,
        y=product_column,
        orientation="h",
        title="ТОП материалов по стоимости"
    )

    fig.update_layout(
        height=700
    )

    return fig
