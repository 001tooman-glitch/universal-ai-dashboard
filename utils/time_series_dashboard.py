import pandas as pd


def build_time_series_dashboard(df):

    result = {}

    # ====================================
    # Общая информация
    # ====================================

    result["rows"] = len(df)

    result["periods"] = []

    if "Период" in df.columns:

        result["periods"] = sorted(
            df["Период"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

    # ====================================
    # Показатели
    # ====================================

    numeric_columns = list(
        df.select_dtypes(
            include="number"
        ).columns
    )

    result["metrics"] = numeric_columns

    # ====================================
    # Тренды
    # ====================================

    trends = {}

    if (
        "Период" in df.columns
        and numeric_columns
    ):

        for metric in numeric_columns:

            try:

                trend = (
                    df.groupby("Период")[metric]
                    .sum()
                    .reset_index()
                )

                trends[metric] = trend

            except Exception:

                pass

    result["trends"] = trends

    # ====================================
    # Сравнение периодов
    # ====================================

    comparisons = {}

    if (
        "Период" in df.columns
        and len(result["periods"]) >= 2
    ):

        periods = result["periods"]

        first_period = periods[0]
        last_period = periods[-1]

        df_first = df[
            df["Период"] == first_period
        ]

        df_last = df[
            df["Период"] == last_period
        ]

        for metric in numeric_columns:

            try:

                value_first = (
                    df_first[metric]
                    .sum()
                )

                value_last = (
                    df_last[metric]
                    .sum()
                )

                difference = (
                    value_last
                    - value_first
                )

                percent = 0

                if value_first != 0:

                    percent = round(
                        difference
                        / value_first
                        * 100,
                        2
                    )

                comparisons[metric] = {

                    "first_period": first_period,

                    "last_period": last_period,

                    "first_value": value_first,

                    "last_value": value_last,

                    "difference": difference,

                    "percent": percent
                }

            except Exception:

                pass

    result["comparisons"] = comparisons

    # ====================================
    # Инсайты
    # ====================================

    insights = []

    insights.append(
        f"Количество периодов: {len(result['periods'])}"
    )

    insights.append(
        f"Количество числовых показателей: {len(numeric_columns)}"
    )

    if len(result["periods"]) > 1:

        insights.append(
            "Доступен анализ динамики и сравнение периодов."
        )

    result["insights"] = insights

    return result
