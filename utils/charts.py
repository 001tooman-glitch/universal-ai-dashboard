import plotly.express as px

def build_chart(df, metric, dimension):

    chart_data = (
        df.groupby(dimension)[metric]
        .sum()
        .reset_index()
        .sort_values(
            metric,
            ascending=False
        )
        .head(15)
    )

    fig = px.bar(
        chart_data,
        x=dimension,
        y=metric,
        text=metric,
        title=f"{metric} по {dimension}"
    )

    return fig
