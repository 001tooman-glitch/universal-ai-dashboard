def build_executive_summary(
    dashboard
):
    """
    Формирует краткую управленческую сводку
    для руководителя на основании
    результатов анализа.
    """

    summary = []

    passport = dashboard.get(
        "data_passport",
        {}
    )

    domain = passport.get(
        "domain",
        "Не определен"
    )

    summary.append(
        f"Обнаружен домен: {domain}."
    )

    # ====================================
    # ABC/XYZ Matrix
    # ====================================

    analysis_results = dashboard.get(
        "analysis_results",
        []
    )

    for result in analysis_results:

        analysis_id = result.get(
            "analysis_id"
        )

        if analysis_id != "abc_xyz_matrix":

            continue

        if not result.get(
            "success",
            False
        ):

            continue

        data = result.get(
            "data",
            {}
        )

        summary_df = data.get(
            "summary"
        )

        if summary_df is None:

            continue

        try:

            summary_map = {}

            for _, row in summary_df.iterrows():

                group = str(
                    row.iloc[0]
                )

                count = int(
                    row.iloc[1]
                )

                summary_map[
                    group
                ] = count

            if "AX" in summary_map:

                summary.append(
                    f"Группа AX содержит "
                    f"{summary_map['AX']} "
                    f"приоритетных позиций "
                    f"для контроля."
                )

            if "CZ" in summary_map:

                summary.append(
                    f"Группа CZ содержит "
                    f"{summary_map['CZ']} "
                    f"кандидатов на "
                    f"оптимизацию запасов."
                )

            largest_group = max(
                summary_map,
                key=summary_map.get
            )

            summary.append(
                f"Наибольшая группа: "
                f"{largest_group} "
                f"({summary_map[largest_group]} "
                f"позиций)."
            )

        except Exception:

            pass

    # ====================================
    # Рекомендации Copilot
    # ====================================

    recommendations = dashboard.get(
        "recommendations",
        []
    )

    for item in recommendations[:3]:

        if item not in summary:

            summary.append(item)

    # ====================================
    # Инсайты модели
    # ====================================

    insights = dashboard.get(
        "model_insights",
        []
    )

    for item in insights:

        if (
            "анализ" in item.lower()
            or "тренд" in item.lower()
        ):

            summary.append(
                item
            )

    # ====================================
    # Удаление дублей
    # ====================================

    summary = list(
        dict.fromkeys(
            summary
        )
    )

    return summary
