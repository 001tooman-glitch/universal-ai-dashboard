import streamlit as st
import pandas as pd
import numpy as np

from utils.profiler import build_profile
from utils.domain_detector import detect_domain
from utils.recommendations import get_recommendations
from utils.charts import build_chart

st.set_page_config(
    page_title="Universal AI Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Universal AI Dashboard")
st.write("Универсальная платформа анализа данных")

uploaded_file = st.file_uploader(
    "Загрузите Excel или CSV файл",
    type=["xlsx", "csv"]
)

if uploaded_file:

    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Строк", len(df))
    col2.metric("Столбцов", len(df.columns))
    col3.metric("Пропусков", int(df.isna().sum().sum()))
    col4.metric("Дубликатов", int(df.duplicated().sum()))

    domain = detect_domain(df)

    st.subheader("🤖 Предметная область")
    st.success(domain)

    st.subheader("💡 Рекомендованные анализы")

    for rec in get_recommendations(domain):
        st.write(f"✅ {rec}")

    st.subheader("📄 Предпросмотр данных")
    st.dataframe(df.head(100))

    st.subheader("🧩 Структура данных")
    st.dataframe(build_profile(df))

    numeric_cols = list(
        df.select_dtypes(
            include=np.number
        ).columns
    )

    category_cols = list(
        df.select_dtypes(
            include="object"
        ).columns
    )

    if numeric_cols and category_cols:

        st.subheader("📊 Визуализация")

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
        "Загрузите Excel или CSV файл."
    )
