import streamlit as st
import pandas as pd

from utils.kpi_dashboard import build_dashboard_kpis
from utils.dashboard_kpi_renderer import render_priority_kpis
from utils.executive_summary import build_executive_summary
from utils.trend_dashboard import build_trend_chart
from utils.top_materials import build_top_materials

from utils.chart_factory import (
    build_abc_chart,
    build_xyz_chart,
    build_abc_xyz_heatmap
)


def render_copilot_dashboard(dashboard):

    source_df = dashboard.get(
        "source_df"
    )

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

    # ====================================
    # ОБЗОР
    # ====================================

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

                st.subheader(
                    "🔥 ТОП-20 материалов"
                )

                st.dataframe(
                    top_df,
                    use_container_width=True
                )

        except Exception as e:

            st.warning(
                f"Top20: {e}"
            )

    # ====================================
    # ЗАПАСЫ
    # ========================
        with tab2:

        st.subheader(
            "📦 Аналитика запасов"
        )

        try:
                        for result in results:

                analysis_id = result.get(
                    "analysis_id",
                    ""
                )

                success = result.get(
                    "success",
                    False
                )

                data = result.get(
                    "data"
                )

                if not success:

                    continue

                if (
                    analysis_id == "abc_xyz_matrix"
                    and isinstance(
                        data,
                        dict
                    )
                ):

                    st.subheader(
                        "🧩 Матрица ABC/XYZ"
                    )

                    matrix = data.get(
                        "matrix"
                    )

                    if matrix is not None:

                        fig = build_abc_xyz_heatmap(
                            matrix
                        )

                        st.plotly_chart(
                            fig,
                            use_container_width=True
                        )

                    summary_df = data.get(
                        "summary"
                    )

                    if summary_df is not None:

                        with st.expander(
                            "Сводка ABC/XYZ"
                        ):

                            st.dataframe(
                                summary_df,
                                use_container_width=True
                            )

                elif (
                    analysis_id == "abc_analysis"
                    and isinstance(
                        data,
                        pd.DataFrame
                    )
                ):

                    st.subheader(
                        "📦 ABC-анализ"
                    )

                    fig = build_abc_chart(
                        data
                    )

                    st.plotly_chart(
                        fig,
                        use_container_width=True
                    )

                    with st.expander(
                        "Детализация ABC"
                    ):

                        st.dataframe(
                            data.head(100),
                            use_container_width=True
                        )

                elif (
                    analysis_id == "xyz_analysis"
                    and isinstance(
                        data,
                        pd.DataFrame
                    )
                ):

                    st.subheader(
                        "📦 XYZ-анализ"
                    )

                    fig = build_xyz_chart(
                        data
                    )

                    st.plotly_chart(
                        fig,
                        use_container_width=True
                    )

                    with st.expander(
                        "Детализация XYZ"
                    ):

                        st.dataframe(
                            data.head(100),
                            use_container_width=True
                        )

        except Exception as e:

            st.warning(
                f"Запасы: {e}"
            )

    # ====================================
    # ДИАГНОСТИКА
    # ====================================

    with tab3:

        st.subheader(
            "⚙ Диагностика"
        )

        passport = dashboard.get(
            "data_passport",
            {}
        )

        st.json(
            passport
        )
