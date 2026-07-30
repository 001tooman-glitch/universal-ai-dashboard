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
from utils.business_rules import evaluate_business_rules
from utils.abc_analyzer import run_abc_analysis

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

    business_rules = evaluate_business_rules(
        df,
        domain,
        scenario,
        semantics
    )

    # ====================================
    # ПАСПОРТ АНАЛИЗА
    # ====================================

    st.subheader("🧠 Паспорт анализа")

    c1, c2, c3 = st.columns(3)

    c1.metric("Сценарий", scenario)
    c2.metric("Область", domain)
    c3.metric("Записей", len(df))

    # ====================================
    # ИНСАЙТЫ
    # ====================================

    st.subheader(
        "🤖 Автоматические инсайты"
    )

    for insight in insights:

        st.info(insight)

    # ====================================
    # БИЗНЕС-ПРАВИЛА
    # ====================================

    st.subheader(
        "📋 Бизнес-правила и возможности анализа"
    )

    for rule in business_rules:

        st.success(rule)

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
    # ABC АНАЛИЗ
    # ====================================

    product_cols = [
        col
        for col, role in semantics.items()
        if role == "product"
    ]

    amount_cols = [
        col
        for col, role in semantics.items()
        if role == "amount"
    ]

    if product_cols and amount_cols:

        st.subheader(
            "📊 ABC-анализ"
        )

        product_col = product_cols[0]
        amount_col = amount_cols[0]

        try:

            abc_df = run_abc_analysis(
                df,
                product_col,
                amount_col
            )

            abc_summary = (
                abc_df.groupby("ABC")
                .size()
                .reset_index(name="Количество")
            )

            st.
