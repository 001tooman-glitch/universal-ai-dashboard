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

from utils.executive_summary import (
    build_executive_summary
)

from utils.trend_dashboard import (
    build_trend_chart
)

from utils.top_materials import (
    build_top_materials
)

from utils.top_materials_chart import (
    build_top_materials_chart
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
    # EXECUTIVE SUMMARY
    # ====================================

    try:

        summary = build_executive_summary(
            dashboard
        )

        if summary:

            st.subheader(
                "🤖 Executive Summary"
            )

            for item in summary:

                st.success(item)

    except Exception as e:

        st.warning(
            f"Ошибка Executive Summary: {e}"
        )

    # ====================================
    # ДИНАМИКА
    # ====================================

    try:

        if (
            source_df is not None
            and semantic_model
        ):

            fig = build_trend_chart(
                source_df,
                semantic_model
            )

            if fig is not None:

                st.subheader(
                    "📈 Динамика стоимости"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

    except Exception as e:

        st.warning(
            f"Ошибка графика динамики: {e}"
        )

    # ====================================
    # ТОП МАТЕРИАЛОВ
    # ====================================

    try:

        if (
            source_df is not None
            and semantic_model
        ):

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

                product_column = (
                    entities["product"][0]
                )

                amount_column = (
                    entities["amount"][0]
                )

                fig = (
                    build_top_materials_chart(
                        top_df,
                        product_column,
                        amount_column
                    )
                )

                st.subheader(
                    "🔥 ТОП-20 материалов"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

                with st.expander(
                    "Детализация ТОП-20"
                ):

                    st.dataframe(
                        top_df,
                        use_container_width=True
                    )

    except Exception as e:

        st.warning(
            f"Ошибка ТОП материалов: {e}"
        )

    # ====================================
    # АНАЛИТИКА
    # ====================================

    st.subheader(
        "📊 Аналитика"
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
            # ABC XYZ
            # ==========================

            if (
                analysis_id
                == "abc_xyz_matrix"
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

                summary_df = data.get(
                    "summary"
                )

                if matrix is not None:

                    try:

                        fig = (
                            build_abc_xyz_heatmap(
                                matrix
                            )
                        )

                        st.plotly_chart(
                            fig,
                            use_container_width=True
                        )

                    except Exception as e:

                        st.warning(
                            f"Ошибка Heatmap: {e}"
                        )

                if summary_df is not None:

                    with st.expander(
                        "Сводка ABC/XYZ"
                    ):

                        st.dataframe(
                            summary_df,
                            use_container_width=True
                        )

            # ==========================
            # ABC
            # ==========================

            elif (
                analysis_id
                == "abc_analysis"
                and isinstance(
                    data,
                    pd.DataFrame
                )
            ):

                st.subheader(
                    "📦 ABC-анализ"
                )

                try:

                    fig = build_abc_chart(
                        data
                    )

                    st.plotly_chart(
                        fig,
                        use_container_width=True
                    )

                except Exception as e:

                    st.warning(
                        f"Ошибка ABC: {e}"
                    )

                with st.expander(
                    "Детализация ABC"
                ):

                    st.dataframe(
                        data.head(100),
                        use_container_width=True
                    )

            # ==========================
            # XYZ
            # ==========================

            elif (
                analysis_id
                == "xyz_analysis"
                and isinstance(
                    data,
                    pd.DataFrame
                )
            ):

                st.subheader(
                    "📦 XYZ-анализ"
                )

                try:

                    fig = build_xyz_chart(
                        data
                    )

                    st.plotly_chart(
                        fig,
                        use_container_width=True
                    )

                except Exception as e:

                    st.warning(
                        f"Ошибка XYZ: {e}"
                    )

                with st.expander(
                    "Детализация XYZ"
                ):

                    st.dataframe(
                        data.head(100),
                        use_container_width=True
                    )

            # ==========================
            # INVENTORY
            # ==========================

            elif (
                analysis_id
                == "inventory_analysis"
                and isinstance(
                    data,
                    dict
                )
            ):

                insights = data.get(
                    "insights",
                    []
                )

                if insights:

                    st.subheader(
                        "📋 Инсайты по запасам"
                    )

                    for insight in insights:

                        st.info(
                            insight
                        )

    # ====================================
    # ДИАГНОСТИКА
    # ====================================

    st.subheader(
        "⚙ Диагностика"
    )

    passport = dashboard.get(
        "data_passport",
        {}
    )

    with st.expander(
        "AI Паспорт"
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

    with st.expander(
        "Объяснение домена"
    ):

        for item in dashboard.get(
            "domain_explanations",
            []
        ):

            st.write(item)

    with st.expander(
        "Инсайты модели данных"
    ):

        for item in dashboard.get(
            "model_insights",
            []
        ):

            st.write(item)

    with st.expander(
        "Доступные анализы"
    ):

        analyses = dashboard.get(
            "available_analyses",
            []
        )

        if analyses:

            st.dataframe(
                pd.DataFrame(
                    analyses
                ),
                use_container_width=True
            )

    with st.expander(
        "План анализа"
    ):

        plan = dashboard.get(
            "analysis_plan",
            []
        )

        if plan:

            st.dataframe(
                pd.DataFrame(
                    plan
                ),
                use_container_width=True
            )

    with st.expander(
        "Рекомендации Copilot"
    ):

        recommendations = dashboard.get(
            "recommendations",
            []
        )

        for item in recommendations:

            st.write(item)
