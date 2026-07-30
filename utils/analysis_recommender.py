def recommend_analyses(domain, scenario, semantics):

    semantic_values = set(
        semantics.values()
    )

    recommendations = []

    # ====================================
    # Временные ряды
    # ====================================

    if scenario == "time_series":

        recommendations.extend([
            "Динамика показателей",
            "Сравнение периодов",
            "Анализ трендов",
            "Анализ изменений",
            "Прогнозирование"
        ])

    # ====================================
    # Склад
    # ====================================

    if domain == "Склад и запасы":

        recommendations.extend([
            "ABC-анализ материалов",
            "XYZ-анализ",
            "ТОП материалов по стоимости",
            "Анализ подразделений",
            "Поиск неликвидов",
            "Анализ динамики запасов"
        ])

    # ====================================
    # Продажи
    # ====================================

    if domain == "Продажи":

        recommendations.extend([
            "ABC-анализ клиентов",
            "ABC-анализ товаров",
            "Анализ продаж по периодам",
            "Сезонность",
            "RFM-анализ"
        ])

    # ====================================
    # Бюджетирование
    # ====================================

    if domain == "Бюджетирование":

        recommendations.extend([
            "План-Факт анализ",
            "Анализ отклонений",
            "Исполнение бюджета",
            "Структура расходов"
        ])

    # ====================================
    # Семантические правила
    # ====================================

    if (
        "product" in semantic_values
        and "amount" in semantic_values
    ):

        recommendations.extend([
            "ТОП объектов по стоимости",
            "Структурный анализ"
        ])

    if (
        "product" in semantic_values
        and "amount" in semantic_values
        and "date" in semantic_values
    ):

        recommendations.extend([
            "Динамика по объектам",
            "Рост и снижение показателей"
        ])

    if (
        "plan" in semantic_values
        and "actual" in semantic_values
    ):

        recommendations.extend([
            "План-Факт",
            "Отклонения по подразделениям"
        ])

    # ====================================
    # Удаление дублей
    # ====================================

    recommendations = list(
        dict.fromkeys(recommendations)
    )

    if not recommendations:

        recommendations = [
            "Статистический анализ",
            "ТОП-анализ",
            "Корреляционный анализ"
        ]

    return recommendations
