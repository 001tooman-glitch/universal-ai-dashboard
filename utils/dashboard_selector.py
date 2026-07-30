def select_dashboard(domain, scenario, semantics):

    semantic_values = set(
        semantics.values()
    )

    if scenario == "time_series":

        return {
            "name": "Time Series Dashboard",
            "charts": [
                "trend",
                "period_compare",
                "period_kpi"
            ]
        }

    if domain == "Склад и запасы":

        return {
            "name": "Inventory Dashboard",
            "charts": [
                "abc",
                "top_materials",
                "departments"
            ]
        }

    if domain == "Продажи":

        return {
            "name": "Sales Dashboard",
            "charts": [
                "top_customers",
                "top_products",
                "sales_trend"
            ]
        }

    if domain == "Бюджетирование":

        return {
            "name": "Budget Dashboard",
            "charts": [
                "plan_fact",
                "variance"
            ]
        }

    if (
        "amount" in semantic_values
        and "date" in semantic_values
    ):

        return {
            "name": "Financial Dashboard",
            "charts": [
                "amount_trend"
            ]
        }

    return {
        "name": "Generic Dashboard",
        "charts": [
            "distribution",
            "top_values"
        ]
    }
