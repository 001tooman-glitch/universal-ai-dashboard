import streamlit as st


def find_column(df, keywords):

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

    filtered_df = df.copy()

    st.sidebar.header(
        "🎛 Фильтры"
    )

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

    # ==========================
    # ПЕРИОД
    # ==========================

    if (
        date_column is not None
        and date_column in filtered_df.columns
    ):

        periods = sorted(
            filtered_df[date_column]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_periods = (
            st.sidebar.multiselect(
                "📅 Период",
                periods,
                placeholder="Выберите период"
            )
        )

        if selected_periods:

            filtered_df = filtered_df[
                            filtered_df[product_column]
            .astype(str)
            .isin(selected_products)
        ]

    st.sidebar.markdown(
        "---"
    )

    st.sidebar.metric(
        "Записей",
        len(filtered_df)
    )

    st.sidebar.metric(
        "Столбцов",
        len(filtered_df.columns)
    )

    return filtered_df
