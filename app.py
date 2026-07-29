import streamlit as st
import pandas as pd
import numpy as np

from utils.profiler import build_profile
from utils.domain_detector import detect_domain
from utils.recommendations import get_recommendations
from utils.charts import build_chart
from utils.relationships import detect_relationships
from utils.scenario_detector import detect_scenario
from utils.time_series import combine_tables

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

    # ===================================
    # Загрузка файлов
    # ===================================

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

    # ===================================
    # Определение сценария
    # ===================================

    scenario = detect_scenario(tables)

    st.subheader("🧠 Определение сценария")

    if scenario == "time_series":

        st.success(
            "Обнаружены файлы одинаковой структуры. Включен режим анализа периодов."
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
                "Периодов",
                merged_df["Период"].nunique()
            )

        st.subheader("📅 Загруженные периоды")

        periods = (
            merged_df["Период"]
            .value_counts()
            .reset_index()
        )

        periods.columns = [
            "Период",
            "Записей"
        ]

        st.dataframe(
            periods,
            use_container_width=True
        )

        df = merged_df

    elif scenario == "relational":

        st.success(
            "Обнаружены файлы разной структуры. Включен режим поиска связей."
        )

        st.subheader("📂 Загруженные таблицы")

        info = []

        for name, table in tables.items():

            info.append({
                "Таблица": name,
                "Строк": len(table),
                "Столбцов": len(table.columns)
            })

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

    # ===================================
    # KPI
    # ===================================

    st.subheader("📈 KPI")

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

    # ===================================
    # Область данных
    # ===================================

    domain = detect_domain(df)

    st.subheader("🤖 Предметная область")

    st.success(domain)

    st.subheader("💡 Рекомендуемые анализы")

    for item in get_recommendations(domain):

        st.write(f"✅ {item}")

    # ===================================
    # Данные
    # ===================================

    st.subheader("📄 Предпросмотр данных")

    st.dataframe(
        df.head(100),
        use_container_width=True
    )

    # ===================================
    # Структура
    # ===================================

    st.subheader("🧩 Структура данных")

    st.dataframe(
        build_profile(df),
        use_container_width=True
    )

 
