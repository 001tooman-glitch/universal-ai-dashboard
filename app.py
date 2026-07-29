import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# =====================================
# НАСТРОЙКА
# =====================================

st.set_page_config(
    page_title="Universal AI Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Universal AI Dashboard")
st.write("Универсальная платформа анализа данных")

# =====================================
# ФУНКЦИИ
# =====================================

def detect_domain(df):

    cols = " ".join(
        [str(c).lower() for c in df.columns]
    )

    if any(x in cols for x in [
        "материал",
        "остаток",
        "склад",
        "цех"
    ]):
        return "Склад и запасы"

    if any(x in cols for x in [
        "план",
        "факт",
        "бюджет",
        "затраты"
    ]):
        return "Бюджетирование"

    if any(x in cols for x in [
        "выручка",
        "продажи",
        "товар",
        "клиент"
    ]):
        return "Продажи"

    return "Не определено"


def get_recommendations(domain):

    mapping = {

        "Склад и запасы": [
            "ABC-анализ",
            "XYZ-анализ",
            "Анализ остатков"
        ],

        "Бюджетирование": [
            "План-Факт",
            "Отклонения",
            "Структура расходов"
        ],

        "Продажи": [
            "ABC клиентов",
            "ABC товаров",
            "Сезонность"
        ]
    }

    return mapping.get(
        domain,
        ["Статистика", "ТОП-анализ"]
    )


def build_profile(df):

    return pd.DataFrame({
        "Поле": df.columns,
        "Тип": [str(df[c].dtype) for c in df.columns],
        "Пропуски": [df[c].isna().sum() for c in df.columns],
        "Уникальных": [df[c].nunique() for c in df.columns]
    })


# =====================================
# ЗАГРУЗКА ФАЙЛОВ
# =====================================

uploaded_files = st.file_uploader(
    "Загрузите один или несколько файлов",
    type=["xlsx", "csv"],
    accept_multiple_files=True
)

tables = {}

# =====================================
# ОБРАБОТКА
# =====================================

if uploaded_files:

    for file in
