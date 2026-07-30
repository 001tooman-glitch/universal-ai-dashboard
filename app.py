import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from utils.profiler import build_profile
from utils.domain_detector import detect_domain
from utils.recommendations import get_recommendations
from utils.charts import build_chart
from utils.relationships import detect_relationships
from utils.scenario_detector import detect_scenario
from utils.time_series import combine_tables
from utils.periods import sort_periods

st.set_page_config(
    page_title="Universal AI Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Universal AI Dashboard")
st.write("Универсальная платформа анализа данных")

uploaded_files = st.file_uploader(
    "Загрузите один или несколько файлов",
    type=["xlsx", "csv"],
    accept_multiple_files=True
)

tables = {}

if uploaded_files:

    for file in uploaded_files:

        try:

            if file.name.endswith(".csv"):
                df = pd.read_csv(file)
            else:
                df = pd.read_excel(file)

            table_name = (
                file.name
                .replace(".xlsx", "")
                .replace(".csv", "")
            )

            tables[table_name] = df

        except Exception as e:

            st.error(
                f"Ошибка загрузки {file.name}: {e}"
            )

    st.success(
        f"Загружено файлов: {len(tables)}"
    )

    scenario = detect_scenario(tables)

    st.subheader("🧠 Определение сценария")

    if scenario == "time_series":

        st.success(
            "Обнаружены файлы одинаковой структуры. Выполняется анализ периодов."
        )

        merged_df = combine_tables(tables)

        c1, c2 = st.columns(2)

        c1.metric(
            "Всего записей",
            f"{len(merged_df):,}"
        )

        c2.metric(
            "Периодов",
            merged_df["Период"].nunique()
        )

        st.subheader("📅 Периоды")

        periods = (
            merged_df["Период"]
            .value_counts()
            .reset_index()
        )

        periods.columns = [
            "Период",
            "Количество записей"
        ]

        st.dataframe(
            periods,
            use_container_width=True
        )

        # =====================================
        # ДИНАМИКА СТОИМОСТИ
        # =====================================

        if "Общая стоимость" in merged_df.columns:

            st.subheader(
                "📈 Динамика общей стоимости"
            )

            trend = (
                merged_df
                .groupby("Период")["Общая стоимость"]
                .sum()
                .reset_index()
            )

            ordered_periods = sort_periods(
                trend["Период"].tolist()
            )

            trend["Период"] = pd.Categorical(
                trend["Период"],
                categories=ordered_periods,
                ordered=True
            )

            trend = trend.sort_values(
                "Период"
            )

            fig = px.line(
                trend,
                x="Период",
                y="Общая стоимость",
                markers=True,
                title="Динамика общей стоимости"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # =====================================
        # СРАВНЕНИЕ ПЕРИОДОВ
        # =====================================

        st.subheader(
            "📊 Сравнение периодов"
        )

        available_periods = sort_periods(
            merged_df["Период"]
            .unique()
            .tolist()
        )

        if len(available_periods) >= 2:

            col1, col2 = st.columns(2)

            with col1:

                period_1 = st.selectbox(
                    "Период 1",
                    available_periods,
                    key="period_1"
                )

            with col2:

                period_2 = st.selectbox(
                    "Период 2",
                    available_periods,
                    index=len(
                        available_periods
                    ) - 1,
                    key="period_2"
                )

            df1 = merged_df[
                merged_df["Период"] == period_1
            ]

            df2 = merged_df[
                merged_df["Период"] == period_2
            ]

            if "Общая стоимость" in merged_df.columns:

                value1 = (
                    df1["Общая стоимость"]
                    .sum()
                )

                value2 = (
                    df2["Общая стоимость"]
                    .sum()
                )

                diff = value2 - value1

                pct = 0

                if value1 != 0:

                    pct = (
                        diff
                        / value1
                    ) * 100

                k1, k2, k3, k4 = st.columns(4)

                k1.metric(
                    period_1,
                    f"{value1:,.0f}"
                )

                k2.metric(
                    period_2,
                    f"{value2:,.0f}"
                )

                k3.metric(
                    "Изменение",
                    f"{diff:,.0f}"
                )

                k4.metric(
                    "Изменение %",
                    f"{pct:,.2f}%"
                )

        df = merged_df

    elif scenario == "relational":

        st.success(
            "Обнаружены файлы разной структуры. Выполняется поиск связей."
        )

        info = []

        for name, table in tables.items():

            info.append({

                "Таблица": name,
                "Строк": len(table),
                "Столбцов": len(
                    table.columns
                )
            })

        st.dataframe(
            pd.DataFrame(info),
            use_container_width=True
        )

        relations = detect_relationships(
            tables
        )

        if len(relations):

            st.subheader(
                "🔗 Найденные связи"
            )

            st.dataframe(
                relations,
                use_container_width=True
            )

        selected_table = st.selectbox(
            "Выберите таблицу",
            list(tables.keys())
        )

        df = tables[selected_table]

    else:

        st.info(
            "Загружен один файл."
        )

        df = list(
            tables.values()
        )[0]

    # =====================================
    # KPI
    # =====================================

    st.subheader("📊 KPI")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Строк",
        len(df)
    )

    c2.metric(
        "Столбцов",
        len(df.columns)
    )

    c3.metric(
        "Пропусков",
        int(
            df.isna()
            .sum()
            .sum()
        )
    )

    c4.metric(
        "Дубликатов",
        int(
            df.duplicated()
            .sum()
        )
    )

    # =====================================
    # ОБЛАСТЬ
    # =====================================

    domain = detect_domain(df)

    st.subheader(
        "🎯 Предметная область"
    )

    st.success(domain)

    st.subheader(
        "💡 Рекомендованные анализы"
    )

    for item in get_recommendations(
        domain
    ):

        st.write(
            f"✅ {item}"
        )

    # =====================================
    # ДАННЫЕ
    # =====================================

    st.subheader(
        "📄 Предпросмотр данных"
    )

    st.dataframe(
        df.head(100),
        use_container_width=True
    )

    # =====================================
    # СТРУКТУРА
    # =====================================

    st.subheader(
        "🧩 Структура данных"
    )

    st.dataframe(
        build_profile(df),
        use_container_width=True
    )

    # =====================================
    # ВИЗУАЛИЗАЦИЯ
    # =====================================

    numeric_cols = list(
        df.select_dtypes(
            include=np.number
        ).columns
    )

    category_cols = list(
        df.select_dtypes(
            include=["object"]
        ).columns
    )

    if numeric_cols and category_cols:

        st.subheader(
            "📊 Анализ"
        )

        metric = st.selectbox(
            "Показатель",
            numeric_cols
        )

        dimension = st.selectbox(
            "Измерение",
            category_cols
        )

        fig = build_chart(
            df,
            metric,
            dimension
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

else:

    st.info(
        "Загрузите один или несколько Excel или CSV файлов."
    )
