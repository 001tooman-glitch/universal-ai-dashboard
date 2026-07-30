import streamlit as st


def format_kpi_value(value):

    try:

        value = float(value)

        if abs(value) >= 1_000_000_000:

            return (
                f"{value / 1_000_000_000:.2f} млрд"
            )

        if abs(value) >= 1_000_000:

            return (
                f"{value / 1_000_000:.2f} млн"
            )

        if abs(value) >= 1_000:

            return (
                f"{value:,.0f}"
            )

        return str(round(value, 2))

    except Exception:

        return str(value)


def render_kpi_cards(
    kpis
):

    if not kpis:

        return

    st.subheader(
        "📊 Ключевые показатели"
    )

    columns = st.columns(
        len(kpis)
    )

    for index, (
        name,
        value
    ) in enumerate(
        kpis.items()
    ):

        columns[index].metric(
            label=name,
            value=format_kpi_value(
                value
            )
        )


def render_priority_kpis(
    kpis
):

    if not kpis:

        return

    priority_order = [

        "Общая стоимость",

        "Материалов",

        "Подразделений",

        "Периодов",

        "Записей"
    ]

    filtered = {

        key: kpis[key]

        for key in priority_order

        if key in kpis
    }

    render_kpi_cards(
        filtered
    )
