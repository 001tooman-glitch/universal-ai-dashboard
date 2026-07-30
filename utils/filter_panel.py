import streamlit as st
import pandas as pd


def render_filter_panel(
    df,
    semantic_model
):
    """
    Отображает левую панель фильтров
    и возвращает отфильтрованный DataFrame.
    """

    filtered_df = df.copy()

    entities = semantic_model.get(
        "entities",
        {}
    )

    st.sidebar.header(
        "🎛 Фильтры"
    )

    # ====================================
    # ПЕРИОД
    # ====================================

    if "date" in entities:

        try:

            date_column = (
                entities["date"][0]
            )

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
                    "Период",
                    periods
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

        except Exception:

            pass

    # ====================================
    # МАТЕРИАЛ
    # ====================================

    if "product" in entities:

        try:

            product_column = (
                entities["product"][0]
            )

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
                    "Материал",
                    products
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

        except Exception:

            pass

    # ====================================
    # ПОДРАЗДЕЛЕНИЕ
    # ====================================

    if "department" in entities:

        try:

            department_column = (
                entities["department"][0]
            )

            departments = sorted(
                filtered_df[
                    department_column
                ]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )

            selected_departments = (
                st.sidebar.multiselect(
                    "Подразделение",
                    departments
                )
            )

            if selected_departments:

                filtered_df = filtered_df[
                    filtered_df[
                        department_column
                    ]
                    .astype(str)
                    .isin(
                        selected_departments
                    )
                ]

        except Exception:

            pass

    st.sidebar.markdown("---")

    st.sidebar.metric(
        "Записей",
        len(filtered_df)
    )

    return filtered_df
