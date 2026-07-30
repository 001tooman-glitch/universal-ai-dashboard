import pandas as pd


def build_dashboard_kpis(
    df,
    semantic_model
):

    result = {}

    entities = semantic_model.get(
        "entities",
        {}
    )

    # =========================
    # Общая стоимость
    # =========================

    if "amount" in entities:

        try:

            amount_col = (
                entities["amount"][0]
            )

            result[
                "Общая стоимость"
            ] = round(

                pd.to_numeric(
                    df[amount_col],
                    errors="coerce"
                ).sum(),

                2
            )

        except Exception:

            pass

    # =========================
    # Количество объектов
    # =========================

    if "product" in entities:

        try:

            product_col = (
                entities["product"][0]
            )

            result[
                "Материалов"
            ] = df[
                product_col
            ].nunique()

        except Exception:

            pass

    # =========================
    # Подразделения
    # =========================

    if "department" in entities:

        try:

            dep_col = (
                entities["department"][0]
            )

            result[
                "Подразделений"
            ] = df[
                dep_col
            ].nunique()

        except Exception:

            pass

    # =========================
    # Периоды
    # =========================

    if "date" in entities:

        try:

            date_col = (
                entities["date"][0]
            )

            result[
                "Периодов"
            ] = df[
                date_col
            ].nunique()

        except Exception:

            pass

    result["Записей"] = len(df)

    return result
