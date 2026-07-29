import streamlit as st
import pandas as pd
import numpy as np

from utils.profiler import build_profile
from utils.domain_detector import detect_domain
from utils.recommendations import get_recommendations
from utils.charts import build_chart
from utils.relationships import detect_relationships

st.set_page_config(
    page_title="Universal AI Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Universal AI Dashboard")

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

    st.success(
        f"Загружено файлов: {len(tables)}"
    )

    # ====================================
    # СПИСОК ТАБЛИЦ
    # ====================================

    st.subheader("📂 Загруженные таблицы")

    info = []

    for name, df in tables.items():

        info.append({
            "Таблица": name,
            "Строк": len(df),
            "Столбцов": len(df.columns)
        })

    st.dataframe(
        pd.DataFrame(info),
        use_container_width=True
    )

    # ====================================
    # ПОИСК СВЯЗЕЙ
    # ====================================

    if len(tables) > 1:

        st.subheader("🔗 Найденные связи")

        relations = detect_relationships(
            tables
        )

        if len(relations):

            st.dataframe(
                relations,
                use_container_width=True
            )

        else:

            st.info(
                "Связи автоматически не обнаружены"
            )

    # ====================================
    # ВЫБОР ТАБЛИЦЫ
    # ====================================

    selected_table = st.selectbox(
        "Выберите таблицу",
        list(tables.keys())
    )

    df = tables[selected_table]

    # ====================================
    # KPI
    # ====================================

    st.subheader("📈 KPI")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Строк", len(df))
    c2.metric("Столбцов", len(df.columns))
    c3.metric("Пропусков", int(df.isna().sum().sum()))
    c4.metric("Дубликатов", int(df.duplicated().sum()))

    # ====================================
    # ОБЛАСТЬ
    # ====================================

    domain = detect_domain(df)

    st.subheader("🤖 Предметная область")

    st.success(domain)

    # ====================================
    # РЕКОМЕНДАЦИИ
    # ====================================

    st.subheader("💡 Рекомендованные анализы")

    for rec in get_recommendations(domain):

        st.write(f"✅ {rec}")

    # ====================================
    # ДАННЫЕ
    # ====================================

    st.subheader("📄 Предпросмотр")

    st.dataframe(
        df.head(100),
        use_container_width=True
    )

    # ====================================
    # СТРУКТУРА
    # ====================================

    st.subheader("🧩 Структура данных")

    st.dataframe(
        build_profile(df),
        use_container_width=True
    )

    # ====================================
    # ГРАФИКИ
    # ====================================

    numeric_cols = list(
        df.select_dtypes(
            include=np.number
        ).columns
    )

    category_cols = list(
        df.select_dtypes(
            include=["object"]
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
        "Загрузите один или несколько файлов."
    )
