def build_dashboard_summary(
    dashboard
):

    summary = []

    passport = dashboard.get(
        "data_passport",
        {}
    )

    domain = passport.get(
        "domain",
        "Не определен"
    )

    confidence = passport.get(
        "confidence",
        0
    )

    summary.append(
        f"Обнаружен домен: {domain}."
    )

    summary.append(
        f"Уверенность классификации: {round(confidence * 100, 1)}%."
    )

    # ====================================
    # KPI
    # ====================================

    source_df = dashboard.get(
        "source_df"
    )

    if source_df is not None:

        summary.append(
            f"Количество записей: {len(source_df):,}."
        )

        summary.append(
            f"Количество полей: {len(source_df.columns)}."
        )

    # ====================================
    # Анализы
    # ====================================

    analyses = dashboard.get(
        "available_analyses",
        []
    )

    if analyses:

        top_analyses = [

            item.get("name")

            for item in analyses[:5]
        ]

        summary.append(
            "Доступные анализы: "
            + ", ".join(top_analyses)
            + "."
        )

    # ====================================
    # Результаты
    # ====================================

    analysis_results = dashboard.get(
        "analysis_results",
        []
    )

    completed = [

      
