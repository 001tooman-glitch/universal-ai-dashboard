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

# ==================================================
# НАСТРОЙКА
# ==================================================

st.set_page_config(
    page_title="Universal AI Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Universal AI Dashboard")
st.write("Универсальная платформа анализа данных")

# ==================================================
# ЗАГРУЗКА ФАЙЛОВ
# ==================================================

uploaded_files = st.file_uploader(
    "Загрузите один или несколько файлов",
    type=["xlsx", "csv"],
    accept_multiple_files=True
)

tables = {}

# ==================================================
# ОБРАБОТКА
# ==================================================

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

    # =============================================
    # ОПРЕДЕЛЕНИЕ СЦЕНАРИЯ
    # =============================================

    scenario = detect_scenario(tables)

    st.subheader("🧠 Определение сценария")

    if scenario == "time_series":

        st.success(
            "Обнаружены файлы одинаковой структуры. Выполняется анализ периодов."
        )

        merged_df = combine_tables(tables)

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Всего записей",
                f"{len(merged_df):,}"
            )

        with col2:

            st.metric(
                "Количество периодов",
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

        # =========================================
        # ДИНАМИКА СТОИМОСТИ
        # =========================================

        if "Общая стоимость" in merged_df.columns:

            st.subheader("📈 Динамика общей стоимости")

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
                "Столбцов": len(table.columns)
            })

        st.subheader("📂 Загруженные таблицы")

        st.dataframe(
            pd.DataFrame(info),
            use_container_width=True
        )

        relations = detect_relationships(
            tables
        )

        if len(relations):

            st.subheader("🔗 Найденные связи")

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

        df = list(tables.values())[0]

    # =============================================
    # KPI
    # =============================================

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
        int(df.isna().sum().sum())
    )

    c4.metric(
        "Дубликатов",
        int(df.duplicated().sum())
    )

    # =============================================
    # ПРЕДМЕТНАЯ ОБЛАСТЬ
    # =============================================

    domain = detect_domain(df)

    st.subheader("🎯 Предметная область")

    st.success(domain)

    # =============================================
    # РЕКОМЕНДАЦИИ
    # =============================================

    st.subheader("💡 Рекомендованные анализы")

    for item in get_recommendations(domain):

        st.write(f"✅ {item}")

    # =============================================
    # ПРЕДПРОСМОТР
    # =============================================

    st.subheader("📄 Предпросмотр данных")

    st.dataframe(
        df.head(100),
        use_container_width=True
    )

    # =============================================
    # СТРУКТУРА
    # =============================================

    st.subheader("🧩 Структура данных")

    st.dataframe(
        build_profile(df),
        use_container_width=True
    )

    # =============================================
    # ВИЗУАЛИЗАЦИЯ
    # =============================================

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

        st.subheader("📈 Анализ")

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
