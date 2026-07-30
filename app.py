import streamlit as st
import pandas as pd

from utils.profiler import build_profile
from utils.domain_detector import detect_domain
from utils.scenario_detector import detect_scenario
from utils.time_series import combine_tables
from utils.semantic_analyzer import analyze_semantics
from utils.semantic_report import build_semantic_report
from utils.kpi_detector import detect_kpis
from utils.kpi_report import build_kpi_report
from utils.analysis_recommender import recommend_analyses
from utils.insight_generator import generate_insights

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

if not uploaded_files:

    st.info(
        "Загрузите Excel или CSV файлы."
    )

else:

    tables = {}

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

    scenario = detect_scenario(tables)

    if scenario == "time_series":

        df = combine_tables(tables)

    elif scenario == "relational":

        table_name = st.selectbox(
            "Выберите таблицу",
            list(tables.keys())
        )

        df = tables[table_name]

    else:

        df = list(
            tables.values()
        )[0]

    domain = detect_domain(df)

    semantics = analyze_semantics(df)

    kpis = detect_kpis(df)

    recommendations = recommend_analyses(
        domain,
        scenario,
        semantics
    )

    insights = generate_insights(
        df,
        domain,
        scenario
    )

    # ====================================
    # ПАСПОРТ АНАЛИЗА
    # ====================================

    st.subheader("🧠 Паспорт анализа")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Сценарий",
        scenario
    )

    c2.metric(
        "Область",
        domain
    )

    c3.metric(
        "Записей",
        len(df)
    )

    # ====================================
    # ИНСАЙТЫ
    # ====================================

    st.subheader(
        "🤖 Автоматические инсайты"
    )

    for insight in insights:

        st.info(insight)

    # ====================================
    # РЕКОМЕНДАЦИИ
    # ====================================

    st.subheader(
        "💡 Рекомендуемые анализы"
    )

    for item in recommendations:

        st.write(f"✅ {item}")

    # ====================================
    # KPI
    # ====================================

    st.subheader(
        "🎯 Автоматически найденные KPI"
    )

    kpi_report = build_kpi_report(
        df,
        kpis
    )

    if len(kpi_report) > 0:

        st.dataframe(
            kpi_report,
            use_container_width=True
        )

    # ====================================
    # СЕМАНТИКА
    # ====================================

    st.subheader(
        "🧠 Семантический анализ"
    )

    semantic_report = build_semantic_report(
        df,
        semantics
    )

    st.dataframe(
        semantic_report,
        use_container_width=True
    )

    # ====================================
    # СТАТИСТИКА
    # ====================================

    st.subheader(
        "📊 Статистика данных"
    )

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

    # ====================================
    # СТРУКТУРА
    # ====================================

    st.subheader(
        "🧩 Структура данных"
    )

    st.dataframe(
        build_profile(df),
        use_container_width=True
    )

    # ====================================
    # ПРЕДПРОСМОТР
    # ====================================

    st.subheader(
        "📄 Предпросмотр"
    )

    st.dataframe(
        df.head(100),
        use_container_width=True
    )
