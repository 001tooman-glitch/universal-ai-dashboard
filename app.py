import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from utils.profiler import build_profile
from utils.domain_detector import detect_domain
from utils.charts import build_chart
from utils.relationships import detect_relationships
from utils.scenario_detector import detect_scenario
from utils.time_series import combine_tables
from utils.periods import sort_periods
from utils.domain_router import route_analysis
from utils.semantic_analyzer import analyze_semantics
from utils.semantic_report import build_semantic_report

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

    scenario = detect_scenario(tables)

    if scenario == "time_series":

        merged_df = combine_tables(tables)
        df = merged_df

    elif scenario == "relational":

        selected_table = st.selectbox(
            "Выберите таблицу",
            list(tables.keys())
        )

        df = tables[selected_table]

    else:

        df = list(tables.values())[0]

    # ====================================
    # ПРЕДМЕТНАЯ ОБЛАСТЬ
    # ====================================

    domain = detect_domain(df)

    route = route_analysis(
        domain,
        scenario
    )

 
