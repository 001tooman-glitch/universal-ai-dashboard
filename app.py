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
    return analyze_semantics(df)


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

st.caption(
    "Универсальная AI-платформа анализа данных"
)

uploaded_files = st.file_uploader(
    "Загрузите Excel или CSV файлы",
    type=["xlsx", "csv"],
    accept_multiple_files=True
)

# ====================================
# WAIT FILES
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

with st.spinner(
    "Загрузка файлов..."
):

    for file in uploaded_files:

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

if not tables:

    st.stop()

# ====================================
# SCENARIO
# ====================================

scenario = detect_scenario(
    tables
)

# ====================================
# BUILD DATASET
# ====================================

with st.spinner(
    "Подготовка данных..."
):

    if scenario == "time_series":

        df = cached_combine_tables(
            tables
        )

    elif scenario == "relational":

        selected_table = st.selectbox(
            "Выберите таблицу",
            list(
                tables.keys()
            )
        )

        df = tables[
            selected_table
        ]

    else:

        df = list(
            tables.values()
        )[0]

# ====================================
# SEMANTICS
# ====================================

with st.spinner(
    "Семантический анализ..."
):

    semantics = (
        cached_semantics(
            df
        )
    )

# ====================================
# FILTERS
# ====================================

filtered_df = (
    render_filter_panel(
        df,
        semantics
    )
)

# ====================================
# DASHBOARD
# ====================================

with st.spinner(
    "Построение дашборда..."
):

    dashboard = (
        cached_dashboard(
            filtered_df,
            semantics,
            scenario
        )
    )

render_copilot_dashboard(
    dashboard
)

# ====================================
# DEBUG
# ====================================

with st.expander(
    "📋 Предпросмотр данных"
):

    st.dataframe(
        filtered_df.head(100),
        use_container_width=True
    )
