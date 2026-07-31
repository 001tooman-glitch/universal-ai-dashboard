import streamlit as st
import pandas as pd

from utils.kpi_dashboard import build_dashboard_kpis
from utils.dashboard_kpi_renderer import render_priority_kpis
from utils.executive_summary import build_executive_summary
from utils.trend_dashboard import build_trend_chart
from utils.top_materials import build_top_materials
from utils.top_materials_chart import build_top_materials_chart

from utils.chart_factory import (
    build_abc_chart,
    build_xyz_chart,
    build_abc_xyz_heatmap
)


def render_copilot_dashboard(dashboard):

    source_df = dashboard.get("source_df")

    semantic_model = dashboard.get(
        "semantic_model",
        {}
    )

    results = dashboard.get(
        "analysis_results",
        []
    )

    tab1, tab2, tab3 = st.tabs(
        [
            "📊 Обзор",
            "📦 Запасы",
            "⚙ Диагностика"
        ]
    )

    # ==================================
    # ОБЗОР
    # ==================================

    with tab1:

        try:

            if source_df is not None:

                kpis = build_dashboard_kpis(
                    source_df,
                    semantic_model
                )

                render_priority_kpis(
                    kpis
                )

        except Exception as e:

            st.warning(
                f"KPI: {e}"
            )

        try:

            summary = build_executive_summary(
                dashboard
            )

            if summary:

                st.subheader(
                    "🤖 Executive Summary"
                )

                for item in summary:

                    st.success(
                        item
                    )

        except Exception as e:

            st.warning(
                f"Summary: {e}"
            )

        try:

            fig = build_trend_chart(
                source_df,
                semantic_model
            )

            if fig is not None:

                st.subheader(
                    "📈 Динамика"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

        except Exception as e:

            st.warning(
                f"Trend: {e}"
            )

        try:

            top_df = build_top_materials(
                source_df,
                semantic_model,
                top_n=20
            )

            if top_df is not None:

                entities = semantic_model.get(
                    "entities",
                    {}
                )

                if (
                    "product" in entities
                    and "amount" in entities
                ):
                                        product_col = (
                        entities["product"][0]
                    )

                    amount_col = (
                        entities["amount"][0]
                    )

                    fig = (
                        build_top_materials_chart(
                            top_df,
                            product_col,
                            amount_col
                        )
                    )

                    st.subheader(
                        "🔥 ТОП-20 материалов"
                    )

                    st.plotly_chart(
                        fig,
                        use_container_width=True
                    )

    # ==================================
    # ЗАПАСЫ
    # ==================================

       with tab3:

        st.subheader(
            "⚙ Диагностика"
        )

        passport = dashboard.get(
            "data_passport",
            {}
        )

        st.json(passport)
        
