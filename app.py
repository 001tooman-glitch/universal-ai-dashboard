import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(
    page_title="Universal AI Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Universal AI Dashboard")
st.write("Универсальная платформа анализа данных")

# ==========================================
# Определение предметной области
# ==========================================

def detect_domain(df):
    cols = " ".join([str(c).lower() for c in df.columns])

    if any(x in cols for x in ["материал", "остаток", "склад", "цех"]):
        return "Склад и запасы"

    if any(x in cols for x in ["план", "факт", "бюджет", "затраты"]):
        return "Бюджетирование"

    if any(x in cols for x in ["выручка", "продажи", "клиент", "товар"]):
        return "Продажи"

    return "Не определено"

# ==========================================
# Загрузка файлов
# ==========================================

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

            name = file.name.replace(".xlsx", "").replace(".csv", "")
            tables[name] = df

        except Exception as e:
            st.error(f"Ошибка загрузки {file.name}: {e}")

    st.success(f"Загружено файлов: {len(tables)}")

    selected_table = st.selectbox(
        "Выберите таблицу",
        list(tables.keys())
    )

    df = tables[selected_table]

    # KPI

    st.subheader("📈 KPI")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Строк", len(df))
    c2.metric("Столбцов", len(df.columns))
    c3.metric("Пропусков", int(df.isnull().sum().sum()))
    c4.metric("Дубликатов", int(df.duplicated().sum()))

    # Область

    domain = detect_domain(df)

    st.subheader("🤖 Предметная область")
    st.success(domain)

    # Предпросмотр

    st.subheader("📄 Данные")

    st.dataframe(
        df.head(100),
        use_container_width=True
    )

    # Структура

    st.subheader("🧩 Структура")

    profile = pd.DataFrame({
        "Поле": df.columns,
        "Тип": [str(df[c].dtype) for c in df.
