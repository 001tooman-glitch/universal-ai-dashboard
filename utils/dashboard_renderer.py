import streamlit as st
import pandas as pd


def render_dashboard(
    dashboard_name,
    dashboard_data
):

    st.subheader(
        f"📊 {dashboard_name}"
    )

    if dashboard_data is None:

        st.warning(
            "Нет данных для отображения."
        )

        return

    # ====================================
    # Inventory Dashboard
    # ====================================

    if dashboard_name == "inventory":

        render_inventory_dashboard(
            dashboard_data
        )

    # ====================================
    # Time Series Dashboard
    # ====================================

    elif dashboard_name == "inventory_time_series":

        render_time_series_dashboard(
            dashboard_data
        )

    # ====================================
    # Generic Dashboard
    # ====================================

    else:

        st.info(
            "Специализированный дашборд не найден."
        )

        st.write(dashboard_data)


def render_inventory_dashboard(
    dashboard_data
):

    st.markdown(
        "### 📦 Складская аналитика"
    )

    insights = dashboard_data.get(
        "insights",
        []
    )

    if insights:

        st.markdown(
            "#### 🤖 Инсайты"
        )

        for insight in insights:

            st.info(insight)

    summary = dashboard_data.get(
        "summary"
    )

    if summary is not None:

        st.markdown(
            "#### 📊 ABC/XYZ Сводка"
        )

        st.dataframe(
            summary,
            use_container_width=True
        )

    abc = dashboard_data.get(
        "abc"
    )

    if abc is not None:

        st.markdown(
            "#### 🅰 ABC-анализ"
        )

        st.dataframe(
            abc.head(100),
            use_container_width=True
        )

    xyz = dashboard_data.get(
        "xyz"
    )

    if xyz is not None:

        st.markdown(
            "#### ✳ XYZ-анализ"
        )

        st.dataframe(
            xyz.head(100),
            use_container_width=True
        )

    matrix = dashboard_data.get(
        "matrix"
    )

    if matrix is not None:

        st.markdown(
            "#### 🧩 Матрица ABC/XYZ"
        )

        st.dataframe(
            matrix.head(100),
            use_container_width=True
        )


def render_time_series_dashboard(
    dashboard_data
):

    st.markdown(
        "### 📈 Анализ временных рядов"
    )

    insights = dashboard_data.get(
        "insights",
        []
    )

    for insight in insights:

        st.info(insight)

    periods = dashboard_data.get(
        "periods",
        []
    )

    if periods:

        periods_df = pd.DataFrame({
            "Периоды": periods
        })

        st.markdown(
            "#### 📅 Периоды"
        )

        st.dataframe(
            periods_df,
            use_container_width=True
        )

    comparisons = dashboard_data.get(
        "comparisons",
        {}
    )

    if comparisons:

        st.markdown(
            "#### ⚖ Сравнение периодов"
        )

        comparison_rows = []

        for metric, data in comparisons.items():

            comparison_rows.append({

                "Показатель": metric,

                "Период 1": data[
                    "first_period"
                ],

                "Период 2": data[
                    "last_period"
                ],

                "Изменение": data[
                    "difference"
                ],

                "%": data[
                    "percent"
                ]
            })

        st.dataframe(
            pd.DataFrame(
                comparison_rows
            ),
            use_container_width=True
        )

    trends = dashboard_data.get(
        "trends",
        {}
    )

    if trends:

        st.markdown(
            "#### 📊 Тренды"
        )

        for metric, trend_df in trends.items():

            with st.expander(
                f"Показатель: {metric}"
            ):

                st.dataframe(
                    trend_df,
                    use_container_width=True
                )
