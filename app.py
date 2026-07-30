import streamlit as st
import pandas as pd
import numpy as np

from utils.profiler import build_profile
from utils.domain_detector import detect_domain
from utils.scenario_detector import detect_scenario
from utils.time_series import combine_tables
from utils.semantic_analyzer import analyze_semantics
from utils.semantic_report import build_semantic_report
from utils.kpi_detector import detect_kpis
from utils.kpi_report import build_kpi_report
from utils.analysis_recommender import recommend_analyses

st.set_page_config(
    page_title="Universal AI Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Universal AI Dashboard")

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

            name = (
                file.name
                .replace(".xlsx", "")
                .replace(".csv", "")
            )

            tables[name] = df

        except Exception as e:

            st.error(
                f"Ошибка загрузки {file.name}: {e}"
            )

    scenario = detect_scenario(tables)

    if scenario == "time_series":

        df = combine_tables(tables)

    elif scenario == "relational":

        selected_table = st.selectbox(
            "Таблица",
            list(tables.keys())
        )

        df = tables[selected_table]

    else:

        df = list(tables.values())[0]

    domain = detect_domain(df)

    semantics = analyze_semantics(df)

    kpis = detect_kpis(df)

    ai_recommendations = recommend_analyses(
        domain,
        scenario,
        semantics
    )

    st.subheader("🧠 Паспорт анализа")

    c1, c2, c3 = st.columns(3)

    c1.metric("Сценарий", scenario)
    c2.metric("Область", domain)
    c3.metric("Записей", len(df))

    st.subheader("🤖 AI рекомендации")

    for item in ai_recommendations:

        st.write(f"✅ {item}")

    st.subheader(
        "🎯 Автоматически найденные KPI"
    )

    kpi_report = build_kpi_report(
        df,
        kpis
    )

    if len(kpi_report):

        st.dataframe(
            kpi_report,
            use_container_width=True
        )

    st.subheader(
        "🧠 Семантический анализ"
    )

    st.dataframe(
        build_semantic_report(
            df,
            semantics
        ),
        use_container_width=True
    )

    st.subheader(
        "📊 Статистика данных"
    )

    k1, k2, k3, k4 = st.columns(4)

    k1.metric(
        "Строк",
        len(df)
    )

    k2.metric(
        "Столбцов",
        len(df.columns)
    )

    k3.metric(
        "Пропусков",
        int(df.isna().sum().sum())
    )

    k4.metric(
        "Дубликатов",
        int(df.duplicated().sum())
    )

    st.subheader(
    "📄 Предпросмотр"
)

st.dataframe(
    df.head(100),
    use_container_width=True
)

