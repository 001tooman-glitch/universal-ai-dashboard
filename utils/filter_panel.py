import streamlit as st


def find_column(df, keywords):
    """
    Поиск колонки по ключевым словам.
    """

    for column in df.columns:

        col = str(column).lower()

        for keyword in keywords:

            if keyword in col:

                return column

    return None


def render_filter_panel(
    df,
    semantic_model=None
):
    """
    Простая универсальная панель фильтров.
    """

    filtered_df = df.copy()

    st.sidebar.header(
        "🎛 Фильтры"
    )

    # ====================================
    # ПОИСК КОЛОНОК
    # ====================================

    date_column = find_column(
        df,
        [
            "период",
            "date",
            "дата"
        ]
    )

    product_column = find_column(
        df,
        [
            "материал",
            "наименование",
            "номенклатура",
            "product"
        ]
    )

    department_column = find_column(
        df,
        [
            "цех",
            "подразделение",
            "department",
            "склад"
        ]
    )

    # ====================================
    # ПЕРИОД
    # ====================================

    if date_column in filtered_df.columns:

        periods = sorted(
            filtered_df[date_column]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_periods = st.sidebar.multiselect(
            "📅 Период",
            periods
        )

        if selected_periods:

            filtered_df = filtered_df[
                filtered_df[date_column]
                .astype(str)
                .isin(selected_periods)
            ]

    # ====================================
    # МАТЕРИАЛ
    # ====================================

    if product_column in filtered_df.columns:

        products = sorted(
            filtered_df[product_column]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_products = st.sidebar.multiselect(
            "📦 Материал",
            products
        )

        if selected_products:

            filtered_df = filtered_df[
                filtered_df[product_column]
                .astype(str)
                .isin(selected_products)
            ]

    # ====================================
    # ПОДРАЗДЕЛЕНИЕ
    # ====================================

    if (
        department_column is not None
        and department_column in filtered_df.columns
    ):

        departments = sorted(
            filtered_df[department_column]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_departments = st.sidebar.multiselect(
            "🏭 Подразделение",
            departments
        )

        if selected_departments:

            filtered_df = filtered_df[
                filtered_df[department_column]
                .astype(str)
                .isin(selected_departments)
            ]

    # ====================================
    # СТАТИСТИКА
    # ====================================

    st.sidebar.markdown("---")

    st.sidebar.metric(
        "Записей",
        len(filtered_df)
    )

    st.sidebar.metric(
        "Столбцов",
        len(filtered_df.columns)
    )

    return filtered_df
