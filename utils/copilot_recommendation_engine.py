def build_copilot_recommendations(
    domain_result,
    semantic_model,
    available_analyses,
    analysis_results=None,
    insights=None
):

    recommendations = []

    domain = domain_result.get(
        "domain",
        "Не определен"
    )

    confidence = domain_result.get(
        "confidence",
        0
    )

    recommendations.append(
        f"Определен домен: {domain}"
    )

    recommendations.append(
        f"Уровень уверенности: {round(confidence * 100, 1)}%"
    )

    # ====================================
    # Рекомендации по анализам
    # ====================================

    if available_analyses:

        top = available_analyses[:3]

        recommendations.append(
            "Рекомендуемые первоочередные анализы:"
        )

        for analysis in top:

            recommendations.append(
                f"• {analysis['name']}"
            )

    # ====================================
    # Анализ модели данных
    # ====================================

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

    if dimensions and measures:

        recommendations.append(
            "Доступен многомерный анализ KPI."
        )

    if dates and measures:

        recommendations.append(
            "Обнаружены временные данные. "
            "Рекомендуется анализ динамики."
        )

    # ====================================
    # Интерпретация выполненных анализов
    # ====================================

    if analysis_results:

        for result in analysis_results:

            if not result.get(
                "success",
                False
            ):
                continue

            analysis_id = result.get(
                "analysis_id"
            )

            if analysis_id == "abc_analysis":

                recommendations.append(
                    "ABC-анализ выполнен. "
                    "Рекомендуется изучить группу A."
                )

            elif analysis_id == "xyz_analysis":

                recommendations.append(
                    "XYZ-анализ выполнен. "
                    "Рекомендуется обратить внимание "
                    "на группу Z."
                )

            elif analysis_id == "abc_xyz_matrix":

                recommendations.append(
                    "Матрица ABC/XYZ построена. "
                    "Приоритетная группа для контроля: AX."
                )

            elif analysis_id == "plan_fact_analysis":

                recommendations.append(
                    "Рекомендуется анализ отклонений "
                    "по плановым и фактическим данным."
                )

    # ====================================
    # Инсайты
    # ====================================

    if insights:

        recommendations.append(
            "Ключевые наблюдения:"
        )

        for insight in insights[:5]:

            recommendations.append(
                f"• {insight}"
            )

    # ====================================
    # Доменная логика
    # ====================================

    if domain == "Склад и запасы":

        recommendations.append(
            "Рекомендуется регулярное "
            "использование ABC/XYZ анализа."
        )

        recommendations.append(
            "Особое внимание стоит уделять "
            "группам AX и AZ."
        )

    elif domain == "Продажи":

        recommendations.append(
            "Рекомендуется анализ клиентов "
            "и продуктового портфеля."
        )

    elif domain == "Бюджетирование":

        recommendations.append(
            "Основной сценарий анализа: "
            "План-Факт и отклонения."
        )

    elif domain == "Финансы":

        recommendations.append(
            "Рекомендуется анализ структуры "
            "затрат и динамики показателей."
        )

    # ====================================
    # Удаление дублей
    # ====================================

    recommendations = list(
        dict.fromkeys(
            recommendations
        )
    )

    return recommendations
