import streamlit as st
import pandas as pd


def render_copilot_dashboard(
    dashboard
):

    # ====================================
    # Паспорт данных
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
    # Объяснение домена
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
    # Инсайты модели данных
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
    # Доступные анализы
    # ====================================

    st.subheader(
        "📚 Доступные анализы"
    )

    analyses = dashboard.get(
        "available_analyses",
        []
    )

    if analyses:

        analyses_df = pd.DataFrame(
            analyses
        )

        st.dataframe(
            analyses_df,
            use_container_width=True
        )

    # ====================================
    # План анализа
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
    # Результаты анализов
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

            with st.expander(
                f"Анализ: {analysis_id}"
            ):

                if not success:

                    st.warning(
                        result.get(
                            "message",
                            "Ошибка выполнения."
                        )
                    )

                    continue

                data = result.get(
                    "data"
                )

                if isinstance(
                    data,
                    pd.DataFrame
                ):

                    st.dataframe(
                        data.head(100),
                        use_container_width=True
                    )

                elif isinstance(
                    data,
                    dict
                ):

                    for name, value in data.items():

                        st.markdown(
                            f"**{name}**"
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

                            st.write(
                                value
                            )

                else:

                    st.write(data)

    # ====================================
    # Рекомендации Copilot
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
