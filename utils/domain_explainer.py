def explain_domain(
    semantic_model,
    classification_result
):

    explanations = []

    domain = classification_result.get(
        "domain",
        "Не определен"
    )

    confidence = classification_result.get(
        "confidence",
        0
    )

    entities = semantic_model.get(
        "entities",
        {}
    )

    explanations.append(
        f"Определенный домен: {domain}"
    )

    explanations.append(
        f"Уверенность: {round(confidence * 100, 1)}%"
    )

    explanations.append(
        "Причины классификации:"
    )

    # ====================================
    # Product
    # ====================================

    if "product" in entities:

        explanations.append(
            "✅ Обнаружены объекты типа product"
        )

    # ====================================
    # Quantity
    # ====================================

    if "quantity" in entities:

        explanations.append(
            "✅ Обнаружены количественные показатели"
        )

    # ====================================
    # Amount
    # ====================================

    if "amount" in entities:

        explanations.append(
            "✅ Обнаружены стоимостные показатели"
        )

    # ====================================
    # Department
    # ====================================

    if "department" in entities:

        explanations.append(
            "✅ Обнаружены подразделения"
        )

    # ====================================
    # Customer
    # ====================================

    if "customer" in entities:

        explanations.append(
            "✅ Обнаружены клиенты или контрагенты"
        )

    # ====================================
    # Date
    # ====================================

    if "date" in entities:

        explanations.append(
            "✅ Обнаружены временные признаки"
        )

    # ====================================
    # Plan / Actual
    # ====================================

    if "plan" in entities:

        explanations.append(
            "✅ Обнаружены плановые показатели"
        )

    if "actual" in entities:

        explanations.append(
            "✅ Обнаружены фактические показатели"
        )

    # ====================================
    # Бизнес-возможности
    # ====================================

    if (
        "product" in entities
        and "amount" in entities
    ):

        explanations.append(
            "📊 Возможен ABC-анализ"
        )

    if (
        "product" in entities
        and "quantity" in entities
    ):

        explanations.append(
            "📊 Возможен XYZ-анализ"
        )

    if (
        "product" in entities
        and "amount" in entities
        and "quantity" in entities
    ):

        explanations.append(
            "📊 Возможна матрица ABC/XYZ"
        )

    if (
        "plan" in entities
        and "actual" in entities
    ):

        explanations.append(
            "📊 Возможен План-Факт анализ"
        )

    if (
        "customer" in entities
        and "amount" in entities
    ):

        explanations.append(
            "📊 Возможен анализ клиентов и продаж"
        )

    return explanations
