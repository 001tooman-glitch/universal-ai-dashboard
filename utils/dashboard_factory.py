def get_dashboard_name(
    domain,
    scenario
):

    if scenario == "time_series":

        return "inventory_time_series"

    if domain == "Склад и запасы":

        return "inventory"

    if domain == "Продажи":

        return "sales"

    if domain == "Бюджетирование":

        return "budget"

    return "generic"


def build_dashboard(
    df,
    domain,
    scenario,
    semantics,
    inventory_dashboard=None
):

    dashboard_name = get_dashboard_name(
        domain,
        scenario
    )

    result = {
        "dashboard": dashboard_name,
        "data": None
    }

    # ==============================
    # Складской дашборд
    # ==============================

    if (
        dashboard_name == "inventory"
        and inventory_dashboard is not None
    ):

        product_columns = [

            col

            for col, role

            in semantics.items()

            if role == "product"
        ]

        amount_columns = [

            col

            for col, role

            in semantics.items()

            if role == "amount"
        ]

        if product_columns and amount_columns:

            result["data"] = inventory_dashboard(
                df,
                product_columns[0],
                amount_columns[0]
            )

    # ==============================
    # Временные ряды
    # ==============================

    elif dashboard_name == "inventory_time_series":

        result["data"] = {
            "type": "time_series",
            "rows": len(df)
        }

    # ==============================
    # Продажи
    # ==============================

    elif dashboard_name == "sales":

        result["data"] = {
            "type": "sales",
            "rows": len(df)
        }

    # ==============================
    # Бюджетирование
    # ==============================

    elif dashboard_name == "budget":

        result["data"] = {
            "type": "budget",
            "rows": len(df)
        }

    # ==============================
    # Универсальный режим
    # ==============================

    else:

        result["data"] = {
            "type": "generic",
            "rows": len(df)
        }

    return result
