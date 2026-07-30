import streamlit as st
import pandas as pd

from utils.chart_factory import (
    build_abc_chart,
    build_xyz_chart,
    build_abc_xyz_heatmap
)

from utils.kpi_dashboard import (
    build_dashboard_kpis
)

from utils.dashboard_kpi_renderer import (
    render_priority_kpis
)


def render_copilot_dashboard(
    dashboard
):

    source_df = dashboard.get(
        "source_df"
    )

    semantic_model = dashboard.get(
        "semantic_model",
        {}
    )

    # ====================================
    # KPI
    # ====================================

    if (
        source_df is not None
        and semantic_model
    ):

        try:

            kpis = build_dashboard_kpis(
                source_df,
                semantic_model
            )

            render_priority_kpis(
                kpis
            )

        except Exception as e:

            st.warning(
                f"Ошибка KPI: {e}"
            )

    # ====================================
    # ПАСПОРТ
    # ====================================

    passport = dashboard.get(
        "data_passport",
        {}
    )

    with st.expander(
        "🧠 AI Паспорт данных"
    ):

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Домен",
            passport.get(
                "domain",
                "-"
            )
        )

        c2.metric(
            "Уверенность",
            f"{round(passport.get('confidence', 0) * 100, 1)}%"
        )

        c3.metric(
            "Измерений",
            passport.get(
                "dimensions",
                0
            )
        )

        c4.metric(
            "Показателей",
            passport.get(
                "measures",
                0
            )
        )

    # ====================================
    # ИНСАЙТЫ
    # ====================================

    recommendations = dashboard.get(
        "recommendations",
        []
    )

    if recommendations:

        st.subheader(
            "🤖 Выводы Copilot"
        )

        for item in recommendations[:10]:

            st.success(item)

    # ====================================
    # АНАЛИЗЫ
    # ====================================

    st.subheader(
        "📊 Визуальная аналитика"
    )

    results = dashboard.get(
        "analysis_results",
        []
    )

    if not results:

        st.info(
            "Нет результатов анализа."
        )

    else:

        for result in results:

            analysis_id = result.get(
                "analysis_id",
                "unknown"
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

            # ==========================
            # 
