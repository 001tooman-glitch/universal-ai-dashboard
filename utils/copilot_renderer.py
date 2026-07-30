import streamlit as st
import pandas as pd

from utils.chart_factory import (
    build_abc_chart,
    build_xyz_chart,
    build_abc_xyz_heatmap
)


def render_copilot_dashboard(
    dashboard
):

    # ====================================
    # ПАСПОРТ
    # ====================================

    passport = dashboard.get(
        "data_passport",
        {}
    )

    st.subheader(
        "🧠 AI Паспорт данных"
    )

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
    # ДОМЕН
    # ====================================

    st.subheader(
        "🎯 Определение домена"
    )

    for item in dashboard.get(
        "domain_explanations",
        []
    ):

        st.info(item)

    # ====================================
    # ИНСАЙТЫ
    # ====================================

    st.subheader(
        "💡 Инсайты модели данных"
    )

    for item in dashboard.get(
        "model_insights",
        []
    ):

        st.success(item)

    # ====================================
    # ДОСТУПНЫЕ АНАЛИЗЫ
    # ====================================

    st.subheader(
        "📚 Доступные анализы"
    )

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

    # ====================================
    # ПЛАН АНАЛИЗА
    # ====================================

    st.subheader(
        "📋 План анализа"
    )

    plan = dashboard.get(
        "analysis_plan",
        []
    )

    if plan:

        st.dataframe(
            pd.DataFrame(plan),
            use_container_width=True
        )

    # ====================================
    # РЕЗУЛЬТАТЫ
    # ====================================

    st.subheader(
        "📊 Выполненные анализы"
    )

    results = dashboard.get(
        "analysis_results",
        []
    )

    if not results:

        st.info(
            "Нет результатов анализа."
        )

        return

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

        with st.expander(
            f"📈 {analysis_id}",
            expanded=True
        ):

            if not success:

                st.warning(
                    result.get(
                        "message",
                        "Ошибка выполнения"
                    )
                )

                continue

            # ======================
            # ABC
            # ======================

            if (
                analysis_id ==
                "abc_analysis"
                and isinstance(
                    data,
                    pd.DataFrame
                )
            ):

                try:

                    fig = (
                        build_abc_chart(
                            data
                        )
                    )

                    st.plotly_chart(
                        fig,
                        use_container_width=True
                    )

                except Exception as e:

                    st.warning(
                        f"Ошибка графика ABC: {e}"
                    )

                st.dataframe(
                    data.head(100),
                    use_container_width=True
                )

                continue

            # ======================
            # XYZ
            # ======================

            if (
                analysis_id ==
                "xyz_analysis"
                and isinstance(
                    data,
                    pd.DataFrame
                )
            ):

                try:

                    fig = (
                        build_xyz_chart(
                            data
                        )
                    )

                    st.plotly_chart(
                        fig,
                        use_container_width=True
                    )

                except Exception as e:

                    st.warning(
                        f"Ошибка графика XYZ: {e}"
                    )

                st.dataframe(
                    data.head(100),
                    use_container_width=True
                )

                continue

            # ======================
            # ABC XYZ
            # ======================

            if (
                analysis_id ==
                "abc_xyz_matrix"
                and isinstance(
                    data,
                    dict
                )
            ):

                matrix = data.get(
                    "matrix"
                )

                summary = data.get(
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
                            f"Ошибка тепловой карты: {e}"
                        )

                if summary is not None:

                    st.dataframe(
                        summary,
                        use_container_width=True
                    )

                if matrix is not None:

                    st.dataframe(
                        matrix.head(100),
                        use_container_width=True
                    )

                continue

            # ======================
            # DataFrame
            # ======================

            if isinstance(
                data,
                pd.DataFrame
            ):

                st.dataframe(
                    data.head(100),
                    use_container_width=True
                )

            # ======================
            # Dict
            # ======================

            elif isinstance(
                data,
                dict
            ):

                for key, value in data.items():

                    st.markdown(
                        f"**{key}**"
                    )

                    if isinstance(
                        value,
                        pd.DataFrame
                    ):

                        st.dataframe(
                            value.head(100),
                            use_container_width=True
                        )

                    else:

                        st.write(value)

            else:

                st.write(data)

    # ====================================
    # РЕКОМЕНДАЦИИ
    # ====================================

    st.subheader(
        "🤖 Рекомендации Copilot"
    )

    recommendations = dashboard.get(
        "recommendations",
        []
    )

    for recommendation in recommendations:

        st.info(
            recommendation
        )
