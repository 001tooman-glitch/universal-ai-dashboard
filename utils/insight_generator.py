def generate_insights(df, domain, scenario):

    insights = []

    insights.append(
        f"Количество записей: {len(df):,}"
    )

    insights.append(
        f"Количество полей: {len(df.columns)}"
    )

    insights.append(
        f"Предметная область: {domain}"
    )

    if scenario == "time_series":

        insights.append(
            "Обнаружен временной ряд. Рекомендуется анализ динамики и сравнение периодов."
        )

    elif scenario == "relational":

        insights.append(
            "Обнаружены таблицы разной структуры. Рекомендуется анализ связей."
        )

    else:

        insights.append(
            "Загружена отдельная таблица."
        )

    return insights
