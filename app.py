import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import duckdb

# =====================================================
# НАСТРОЙКИ
# =====================================================

st.set_page_config(
    page_title="Universal AI Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Universal AI Dashboard MVP 3.0")
st.markdown("Универсальная AI-платформа анализа данных")

# =====================================================
# ФУНКЦИИ
# =====================================================

def detect_domain(df):

    cols = " ".join(
        [str(c).lower() for c in df.columns]
    )

    if any(x in cols for x in [
        "материал",
        "остаток",
        "склад",
        "цех",
        "запас",
        "номенклатура"
    ]):
        return "Склад и запасы"

    if any(x in cols for x in [
        "план",
        "факт",
        "бюджет",
        "затраты",
        "расход"
    ]):
        return "Бюджетирование"

    if any(x in cols for x in [
        "продажи",
        "выручка",
        "клиент",
        "товар"
    ]):
        return "Продажи"

    if any(x in cols for x in [
        "доход",
        "прибыль",
        "расходы"
    ]):
        return "Финансы"

    if any(x in cols for x in [
        "сотрудник",
        "табельный",
        "должность"
    ]):
        return "HR"

    return "Не определено"


def recommendations(domain):

    mapping = {

        "Склад и запасы": [
            "ABC-анализ",
            "XYZ-анализ",
            "Неликвиды",
            "Остатки по подразделениям",
            "Структура запасов"
        ],

        "Бюджетирование": [
            "План-Факт",
            "Отклонения",
            "Структура расходов",
            "Исполнение бюджета"
        ],

        "Продажи": [
            "ABC клиентов",
            "ABC товаров",
            "Сезонность",
            "Прогноз продаж"
        ],

        "Финансы": [
            "Доходы и расходы",
            "Рентабельность",
            "Структура затрат"
        ],

        "HR": [
            "Штатная структура",
            "Численность",
            "Текучесть"
        ]
    }

    return mapping.get(
        domain,
        [
            "Статистика",
            "ТОП объектов",
            "Корреляции"
        ]
    )


def profile_dataframe(df):

    return pd.DataFrame({

        "Поле": df.columns,

        "Тип": [
            str(df[col].dtype)
            for col in df.columns
        ],

        "Пропуски": [
            int(df[col].isnull().sum())
            for col in df.columns
        ],

        "Уникальных": [
            int(df[col].nunique())
            for col in df.columns
  
