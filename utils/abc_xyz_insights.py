def generate_abc_xyz_insights(
    matrix_df,
    summary_df
):

    insights = []

    total_items = len(matrix_df)

    insights.append(
        f"Всего проанализировано объектов: {total_items}"
    )

    for _, row in summary_df.iterrows():

        group_name = row["ABC_XYZ"]

        count = int(row["Количество"])

        share = round(
            count / total_items * 100,
            2
        ) if total_items > 0 else 0

        insights.append(
            f"Группа {group_name}: "
            f"{count} объектов "
            f"({share}%)"
        )

    # ====================================
    # Бизнес-интерпретация
    # ====================================

    group_counts = {
        row["ABC_XYZ"]: int(row["Количество"])
        for _, row in summary_df.iterrows()
    }

    if group_counts.get("AX", 0) > 0:

        insights.append(
            "Группа AX содержит наиболее важные "
            "и стабильные объекты. "
            "Рекомендуется максимальный контроль."
        )

    if group_counts.get("AZ", 0) > 0:

        insights.append(
            "Группа AZ содержит важные объекты "
            "с высокой изменчивостью. "
            "Рекомендуется контроль страховых запасов."
        )

    if group_counts.get("BZ", 0) > 0:

        insights.append(
            "Группа BZ требует дополнительного "
            "анализа причин колебаний."
        )

    if (
        group_counts.get("CZ", 0)
        + group_counts.get("CY", 0)
    ) > 0:

        insights.append(
            "Группы CY и CZ могут содержать "
            "кандидатов на оптимизацию запасов."
        )

    if group_counts.get("CX", 0) > 0:

        insights.append(
            "Группа CX состоит из стабильных "
            "объектов с низким влиянием на общий результат."
        )

    return insights
