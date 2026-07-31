def build_dashboard_summary(
    dashboard
):
    """
    Простая текстовая сводка для дашборда.
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
        f"Домен данных: {domain}"
    )

    source_df = dashboard.get(
        "source_df"
    )

    if source_df is not None:

        summary.append(
            f"Количество записей: {len(source_df)}"
        )

        summary.append(
            f"Количество столбцов: {len(source_df.columns)}"
        )

    analyses = dashboard.get(
        "available_analyses",
        []
    )

    if analyses:

        summary.append(
            f"Доступно анализов: {len(analyses)}"
        )

    return summary
