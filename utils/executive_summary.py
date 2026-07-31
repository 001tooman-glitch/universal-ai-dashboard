def build_executive_summary(
    dashboard
):
    """
    Краткая управленческая сводка.
    """

    summary = []

    passport = dashboard.get(
        "data_passport",
        {}
    )

    domain = passport.get(
        "domain",
        "Не определён"
    )

    summary.append(
        f"Обнаружен домен: {domain}."
    )

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

            groups = {}

            for _, row in summary_df.iterrows():

                group = str(
                    row.iloc[0]
                )

                count = int(
                    row.iloc[1]
                )

                groups[group] = count

            if "AX" in groups:

                summary.append(
                    f"Группа AX содержит {groups['AX']} критичных позиций."
                )

            if "CZ" in groups:

                summary.append(
                    f"Группа CZ содержит {groups['CZ']} кандидатов на оптимизацию запасов."
                )

            largest_group = max(
                groups,
                key=groups.get
            )

            summary.append(
                f"Наибольшая группа: {largest_group} ({groups[largest_group]} позиций)."
            )

        except Exception:

            pass

    recommendations = dashboard.get(
        "recommendations",
        []
    )

    for item in recommendations[:3]:

        if item not in summary:

            summary.append(
                item
            )

    summary = list(
        dict.fromkeys(
            summary
        )
    )

    return summary
