def classify_domain(
    semantic_model,
    scenario=None
):

    entities = semantic_model.get(
        "entities",
        {}
    )

    dimensions = semantic_model.get(
        "dimensions",
        []
    )

    measures = semantic_model.get(
        "measures",
        []
    )

    dates = semantic_model.get(
        "dates",
        []
    )

    # ====================================
    # Временные ряды
    # ====================================

    if scenario == "time_series":

        if (
            "product" in entities
            and "amount" in entities
        ):

            return {
                "domain": "Склад и запасы",
                "confidence": 0.95
            }

        return {
            "domain": "Временные ряды",
            "confidence": 0.90
        }

    # ====================================
    # Склад и запасы
    # ====================================

    inventory_score = 0

    if "product" in entities:
        inventory_score += 3

    if "quantity" in entities:
        inventory_score += 3

    if "amount" in entities:
        inventory_score += 2

    if "department" in entities:
        inventory_score += 1

    if inventory_score >= 6:

        return {
            "domain": "Склад и запасы",
            "confidence": round(
                min(
                    inventory_score / 10,
                    1.0
                ),
                2
            )
        }

    # ====================================
    # Продажи
    # ====================================

    sales_score = 0

    if "customer" in entities:
        sales_score += 4

    if "product" in entities:
        sales_score += 2

    if "amount" in entities:
        sales_score += 2

    if len(dates) > 0:
        sales_score += 1

    if sales_score >= 6:

        return {
            "domain": "Продажи",
            "confidence": round(
                min(
                    sales_score / 10,
                    1.0
                ),
                2
            )
        }

    # ====================================
    # Бюджетирование
    # ====================================

    if (
        "plan" in entities
        and "actual" in entities
    ):

        return {
            "domain": "Бюджетирование",
            "confidence": 0.98
        }

    # ====================================
    # Финансы
    # ====================================

    if (
        "amount" in entities
        and len(measures) > 0
        and len(dimensions) > 0
    ):

        return {
            "domain": "Финансы",
            "confidence": 0.75
        }

    # ====================================
    # Универсальный режим
    # ====================================

    return {
        "domain": "Общий анализ",
        "confidence": 0.50
    }
