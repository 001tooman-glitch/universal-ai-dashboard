import streamlit as st


def find_column(
    df,
    keywords
):
    """
    Поиск колонки по набору ключевых слов.
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
    Универсальная панель фильтров.
    Работает даже если семантика не определена.
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
            "period",
            "date",
            "дата"
        ]
    )

    product_column = find_column(
        df,
        [
            "материал",
            "material",
            "product",
            "номенклатура",
            "наименование"
        ]
    )

    department_column = find_column(
        df,
        [
            "цех",
            "подраздел",
            "department",
            "место хранения",
            "склад"
        ]
    )

    # ====================================
    # ПЕРИОД
    # ====================================

    if (
        date_column is not None
        and date_column in filtered_df.columns
    ):

        periods = sorted(
            filtered_df[
                date_column
            ]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_periods = (
            st.sidebar.multiselect(
                "📅 Период",
    
