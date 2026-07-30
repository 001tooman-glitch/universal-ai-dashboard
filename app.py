import streamlit as st
import pandas as pd

from utils.scenario_detector import (
    detect_scenario
)

from utils.time_series import (
    combine_tables
)

from utils.semantic_analyzer import (
    analyze_semantics
)

from utils.copilot_dashboard import (
    build_copilot_dashboard
)

from utils.copilot_renderer import (
    render_copilot_dashboard
)

from utils.filter_panel import (
    render_filter_panel
)


# ====================================
# CACHE
# ====================================

@st.cache_data(show_spinner=False)
def load_dataframe(
    file_bytes,
    file_name
):

    from io import BytesIO

    data = BytesIO(file_bytes)

    if file_name.lower().endswith(
        ".csv"
    ):

        return pd.read_csv(data)

    return pd.read_excel(data)


@st.cache_data(show_spinner=False)
def cached_semantics(
    df
):

    return analyze_semantics(
        df
    )


@st.cache_data(show_spinner=False)
def cached_dashboard(
    df,
    semantics,
    scenario
):

    return build_copilot_dashboard(
        df=df,
        semantics=semantics,
        scenario=scenario
    )


@st.cache_data(show_spinner=False)
def cached_combine_tables(
    tables
):

    return combine_tables(
        tables
    )


# ====================================
# PAGE
# ====================================

st.set_page_config(
    page_title="Universal AI Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title(
    "📊 Universal AI Dashboard"
)

st.write(
    "Универсальная AI-платформа анализа данных"
)

uploaded_files = st.file_uploader(
    "Загрузите Excel или CSV файлы",
    type=[
        "xlsx",
        "csv"
    ],
    accept_multiple_files=True
)

# ====================================
# EMPTY STATE
# ====================================

if not uploaded_files:

    st.info(
        "Загрузите один или несколько файлов."
    )

    st.stop()

# ====================================
# LOAD FILES
# ====================================

tables = {}
load_errors = []

with st.spinner(
    "Загрузка файлов..."
):

    for file in uploaded_files:

        try:

            file_bytes = file.read()

            df = load_dataframe(
                file_bytes,
                file.name
            )

            table_name = (
                file.name
                .replace(".xlsx", "")
                .replace(".csv", "")
            )

            tables[
                table_name
            ] = df

        except Exception as e:

            load_errors.append(
                f"{file.name}: {e}"
            )

if load_errors:

    st.error(
        "\n".join(load_errors)
    )

if not tables:

    st.stop()

# ====================================
# SCENARIO
# ====================================

scenario = detect_scenario(
    tables
