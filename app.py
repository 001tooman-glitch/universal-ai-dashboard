import streamlit as st
import pandas as pd
import numpy as np

from utils.domain_detector import detect_domain
from utils.profiler import build_profile
from utils.recommendations import get_recommendations
from utils.charts import build_chart

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
                f"Ошибка загрузки {file.name}"
            )

            st.error(str(e))

    st.success(
        f"Загружено таблиц: {len(tables)}"
    )

    selected_table = st.selectbox(
        "Выберите таблицу",
        list(tables.keys())
    )

    df = tables[selected_table]

    st.subheader("📈 KPI")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Строк", len(df))
    c2.metric("Столбцов", len(df.columns))
    c3.metric("Пропусков", int(df.isna().sum().sum()))
    c4.metric("Дубликатов", int(df.duplicated().sum()))

    domain = detect_domain(df)

    st.subheader("🤖 Предметная область")

    st.success(domain)

    st.subheader("💡 Рекомендованные анализы")

    for item in get_recommendations(domain):

        st.write(f"✅ {item}")

    st.subheader("📄 Предпросмотр данных")

    st.dataframe(
        df.head(100),
        use_container_width=True
    )

    st.subheader("🧩 Структура данных")

    profile = build_profile(df)

    st.dataframe(
        profile,
        use_container_width=True
    )

    numeric_cols = list(
        
