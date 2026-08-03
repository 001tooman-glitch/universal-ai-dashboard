import streamlit as st


def find_column(
    df,
    keywords
):

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

    shop_column = find_column(
        df,
        [
            "цех",
            "shop",
            "наименование цеха",
            "цех наименование"
        ]
    )

    pfm_column = find_column(
        df,
        [
            "пфм",
            "pfm",
            "код пфм",
            "номер пфм"
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
                periods,
                placeholder="Выберите период"
            )
        )

        if selected_periods:

            filtered_df = filtered_df[
                filtered_df[
                    date_column
                ]
                .astype(str)
                .isin(
                    selected_periods
                )
            ]

    # ==========================
    # МАТЕРИАЛ
    # ==========================

    if (
        product_column is not None
        and product_column in filtered_df.columns
    ):

        products = sorted(
            filtered_df[
                product_column
            ]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_products = (
            st.sidebar.multiselect(
                "📦 Материал",
                products,
                placeholder="Выберите материал"
            )
        )

        if selected_products:

            filtered_df = filtered_df[
                filtered_df[
                    product_column
                ]
                .astype(str)
                .isin(
                    selected_products
                )
            ]
                # ==========================
    # ЦЕХ
    # ==========================

    if (
        shop_column is not None
        and shop_column in filtered_df.columns
    ):

        shops = sorted(
            filtered_df[
                shop_column
            ]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_shops = (
            st.sidebar.multiselect(
                "🏭 Цех",
                shops,
                placeholder="Выберите цех"
            )
        )

        if selected_shops:

            filtered_df = filtered_df[
                filtered_df[
                    shop_column
                ]
                .astype(str)
                .isin(
                    selected_shops
                )
            ]

    # ==========================
    # ПФМ
    # ==========================

    if (
        pfm_column is not None
        and pfm_column in filtered_df.columns
    ):

        pfms = sorted(
                        filtered_df[
                pfm_column
            ]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_pfms = (
            st.sidebar.multiselect(
                "🏷 ПФМ",
                pfms,
                placeholder="Выберите ПФМ"
            )
        )

        if selected_pfms:

            filtered_df = filtered_df[
                filtered_df[
                    pfm_column
                ]
                .astype(str)
                .isin(
                    selected_pfms
                )
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
