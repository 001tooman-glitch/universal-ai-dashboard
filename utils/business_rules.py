def evaluate_business_rules(
    df,
    domain,
    scenario,
    semantics
):

    results = []

    semantic_values = set(
        semantics.values()
    )

    # ====================================
    # Общие правила
    # ====================================

    results.append(
        f"Обнаружено записей: {len(df):,}"
    )

    results.append(
        f"Обнаружено полей: {len(df.columns)}"
    )

    # ====================================
    # Сценарии
    # ====================================

    if scenario == "time_series":

        results.append(
            "Обнаружен временной ряд."
        )

        results.append(
            "Доступен анализ динамики."
        )

        results.append(
            "Доступно сравнение периодов."
        )

    elif scenario == "relational":

        results.append(
            "Обнаружены таблицы разной структуры."
        )

        results.append(
            "Доступен анализ связей между таблицами."
        )

    else:

        results.append(
            "Обнаружена отдельная таблица."
        )

    # ====================================
    # Склад
    # ====================================

    if domain == "Склад и запасы":

        results.append(
            "Данные относятся к складским запасам."
        )

        results.append(
            "Возможен ABC-анализ."
        )

        results.append(
            "Возможен XYZ-анализ."
        )

        results.append(
            "Возможен анализ неликвидов."
        )

    # ====================================
    # Продажи
    # ====================================

    if domain == "Продажи":

        results.append(
            "Данные относятся к продажам."
        )

        results.append(
            "Возможен ABC-анализ клиентов."
        )

        results.append(
            "Возможен ABC-анализ товаров."
        )

        results.append(
            "Возможен анализ сезонности."
        )

    # ====================================
    # Бюджетирование
    # ====================================

    if domain == "Бюджетирование":

        results.append(
            "Обнаружены данные бюджетирования."
        )

        results.append(
            "Возможен План-Факт анализ."
        )

        results.append(
            "Возможен анализ отклонений."
        )

    # ====================================
    # Семантика
    # ====================================

    if (
        "product" in semantic_values
        and "amount" in semantic_values
    ):

        results.append(
            "Обнаружены объекты и стоимостные показатели."
        )

    if (
        "product" in semantic_values
        and "date" in semantic_values
    ):

        results.append(
            "Доступен анализ динамики объектов."
        )

    if (
        "plan" in semantic_values
        and "actual" in semantic_values
    ):

        results.append(
            "Обнаружены поля План и Факт."
        )

    return results
