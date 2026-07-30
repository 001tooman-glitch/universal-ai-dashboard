import streamlit as st
import pandas as pd

from utils.scenario_detector import detect_scenario
from utils.time_series import combine_tables

from utils.semantic_analyzer import (
    analyze_semantics
)

from utils.copilot_dashboard import (
    build_copilot_dashboard
)

from utils.copilot_renderer import (
    render_copilot_dashboard
)

st.set_page_config(
    page_title="Universal AI Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Universal AI Dashboard")
st.write(
    "Универсальная AI-платформа анализа данных"
)

uploaded_files = st.file_uploader(
    "Загрузите Excel или CSV файлы",
    type=["xlsx", "csv"],
    accept_multiple_files=True
)

if not uploaded_files:

    st.info(
        "Загрузите один или несколько файлов."
    )

else:

    tables = {}

    load_errors = []

    for file in uploaded_files:

        try:

            if file.name.lower().endswith(
                ".csv"
            ):

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

            load_errors.append(
                f"{file.name}: {e}"
            )

    if load_errors:

        st.error(
            "\n".join(load_errors)
        )

    if not tables:

        st.stop()

    scenario = detect_scenario(
        tables
    )

    st.subheader(
        "🔍 Информация о загрузке"
    )

    col1, col2 = st.columns(2)

    col1.metric(
        "Файлов",
        len(tables)
    )

    col2.metric(
        "Сценарий",
        scenario
    )

    try:

        if scenario == "time_series":

            df = combine_tables(
                tables
            )

        elif scenario == "relational":

            selected_table = st.selectbox(
                "Выберите таблицу",
                list(tables.keys())
            )

            df = tables[
                selected_table
            ]

        else:

            df = list(
                tables.values()
            )[0]

        st.subheader(
            "📄 Активный набор данных"
        )

        c1, c2 = st.columns(2)

        c1.metric(
            "Строк",
            len(df)
        )

        c2.metric(
            "Столбцов",
            len(df.columns)
        )

        semantics = analyze_semantics(
            df
        )

        dashboard = (
            build_copilot_dashboard(
                df=df,
                semantics=semantics,
                scenario=scenario
            )
        )

        render_copilot_dashboard(
            dashboard
        )

    except Exception as e:

        st.error(
            f"Ошибка анализа данных: {e}"
        )

    st.subheader(
        "📋 Предпросмотр данных"
    )

    st.dataframe(
        df.head(100),
        use_container_width=True
    )
