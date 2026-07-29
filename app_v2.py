import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ============================================
# НАСТРОЙКА СТРАНИЦЫ
# ============================================

st.set_page_config(
    page_title="Universal AI Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Universal AI Dashboard")
st.markdown("Универсальная платформа анализа данных")

# ============================================
# ЗАГРУЗКА ФАЙЛОВ
# ============================================

uploaded_files = st.file_uploader(
    "Загрузите один или несколько файлов",
    type=["xlsx", "csv"],
    accept_multiple_files=True
)

tables = {}

# ============================================
# ОПРЕДЕЛЕНИЕ ПРЕДМЕТНОЙ ОБЛАСТИ
# ============================================

def detect_domain(df):

    cols = " ".join(
        [str(col).lower() for col in df.columns]
    )

    if any(x in cols for x in [
        "материал",
        "запас",
        "остаток",
        "склад",
        "цех"
    ]):
        return "Склад и запасы"

    if any(x in cols for x in [
        "план",
        "факт",
        "бюджет",
        "расход"
    ]):
        return "Бюджетирование"

    if any(x in cols for x in [
        "продажи",
        "выручка",
        "товар",
        "клиент"
    ]):
        return "Продажи"

    return "Не определено"

# ============================================
# РЕКОМЕНДАЦИИ
# ============================================

def get_recommendations(domain):

    recommendations = {
        "Склад и запасы": [
            "ABC-анализ",
            "XYZ-анализ",
            "Неликвиды",
            "Запасы по подразделениям"
        ],

        "Бюджетирование": [
            "План-Факт анализ",
            "Анализ отклонений",
            "Структура расходов"
        ],

        "Продажи": [
            "ABC клиентов",
            "ABC товаров",
            "Сезонность",
            "Прогноз"
        ]
    }

    return recommendations.get(
        domain,
        [
            "Статистика",
            "ТОП объектов",
            "Корреляции"
        ]
    )

# ============================================
# ОБРАБОТКА ФАЙЛОВ
# ============================================

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
                f"Ошибка чтения файла {file.name}: {e}"
            )

    st.success(
        f"Загружено файлов: {len(tables)}"
    )

    # ========================================
    # СПИСОК ТАБЛИЦ
    # ========================================

    selected_table = st.selectbox(
        "Выберите таблицу",
        list(tables.keys())
    )

    df = tables[selected_table]

    # ========================================
    # KPI
    # ========================================

    st.subheader("📈 KPI")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Строк",
            len(df)
        )

    with col2:
        st.metric(
            "Столбцов",
            len(df.columns)
        )

    with col3:
        st.metric(
            "Пропусков",
            int(df.isnull().sum().sum())
        )

    with col4:
        st.metric(
            "Дубликатов",
            int(df.duplicated().sum())
        )

    # ========================================
    # ПРЕДПРОСМОТР
    # ========================================

    st.subheader("📄 Предпросмотр")

    st.dataframe(
        df.head(100),
        use_container_width=True
    )

    # ========================================
    # СТРУКТУРА ДАННЫХ
    # ========================================

    st.subheader("🧩 Структура данных")

    structure = pd.DataFrame({
        "Поле": df.columns,
        "Тип": [str(df[col].dtype)
                for col in df.columns],
        "Пропуски": [
            int(df[col].isnull().sum())
            for col in df.columns
        ],
        "Уникальных": [
            int(df[col].nunique())
            for col in df.columns
        ]
    })

    st.dataframe(
        structure,
        use_container_width=True
    )

    # ========================================
    # ДОМЕН
    # ========================================

    domain = detect_domain(df)

    st.subheader("🤖 Определение области")

    st.success(
        f"Определена область: {domain}"
    )

    st.subheader("💡 Рекомендованные анализы")

    for item in get_recommendations(domain):

        st.write("✅", item)

    # ========================================
    # ВИЗУАЛИЗАЦИЯ
    # ========================================

    numeric_columns = list(
        df.select_dtypes(
            include=np.number
        ).columns
    )

    category_columns = list(
        df.select_dtypes(
            include="object"
        ).columns
    )

    if (
        len(numeric_columns) > 0 and
        len(category_columns) > 0
    ):

        st.subheader("📊 Визуализация")

        metric = st.selectbox(
            "Показатель",
            numeric_columns
        )

        dimension = st.selectbox(
            "Измерение",
            category_columns
        )

        chart_data = (
            df.groupby(dimension)[metric]
            .sum()
            .reset_index()
            .sort_values(
                metric,
                ascending=False
            )
            .head(15)
        )

        fig = px.bar(
            chart_data,
            x=dimension,
            y=metric,
            text=metric,
            title=f"{metric} по {dimension}"
        )

        fig.update_traces(
            textposition="outside"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # ========================================
    # AI-ПОМОЩНИК MVP
    # ========================================

    st.subheader("🤖 AI Аналитик")

    question = st.text_input(
        "Задайте вопрос о данных"
    )

    if question:

        q = question.lower()

        if "структур" in q:

            st.write(structure)

        elif "област" in q:

            st.info(
                f"Определенная предметная область: {domain}"
            )

        elif "анализ" in q:

            for item in get_recommendations(domain):
                st.write("✅", item)

        else:

            st.warning(
                "Пока я умею отвечать только на вопросы о структуре, области данных и рекомендованных анализах."
            )

else:

    st.info(
        "Загрузите один или несколько Excel или CSV файлов."
    )

