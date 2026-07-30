def generate_data_model_insights(
    semantic_model
):

    insights = []

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

    keys = semantic_model.get(
        "keys",
        []
    )

    unknown = semantic_model.get(
        "unknown",
        []
    )

    # ====================================
    # Общая информация
    # ====================================

    insights.append(
        f"Найдено измерений: {len(dimensions)}"
    )

    insights.append(
        f"Найдено показателей: {len(measures)}"
    )

    insights.append(
        f"Найдено дат: {len(dates)}"
    )

    insights.append(
        f"Найдено потенциальных ключей: {len(keys)}"
    )

    # ====================================
    # Аналитические возможности
    # ====================================

    if dimensions and measures:

        insights.append(
            "Возможен многомерный анализ данных."
        )

        insights.append(
            "Доступно построение KPI по измерениям."
        )

    if dates and measures:

        insights.append(
            "Возможен анализ динамики показателей."
        )

        insights.append(
            "Доступно сравнение периодов."
        )

        insights.append(
            "Доступен анализ трендов."
        )

    if len(dimensions) >= 2:

        insights.append(
            "Возможен анализ по нескольким измерениям."
        )

    if keys:

        insights.append(
            "Обнаружены уникальные идентификаторы."
        )

    if unknown:

        insights.append(
            f"Неопознанных полей: {len(unknown)}"
        )

    # ====================================
    # Складская логика
    # ====================================

    entities = semantic_model.get(
        "entities",
        {}
    )

    if (
        "product" in entities
        and "amount" in entities
    ):

        insights.append(
            "Доступен ABC-анализ."
        )

    if (
        "product" in entities
        and "quantity" in entities
    ):

        insights.append(
            "Доступен XYZ-анализ."
        )

    if (
        "product" in entities
        and "amount" in entities
        and "quantity" in entities
    ):

        insights.append(
            "Доступна матрица ABC/XYZ."
        )

    # ====================================
    # План-Факт
    # ====================================

    if (
        "plan" in entities
        and "actual" in entities
    ):

        insights.append(
            "Обнаружены данные для План-Факт анализа."
        )

    # ====================================
    # Продажи
    # ====================================

    if (
        "customer" in entities
        and "amount" in entities
    ):

        insights.append(
            "Доступен анализ клиентов и продаж."
        )

    return insights
