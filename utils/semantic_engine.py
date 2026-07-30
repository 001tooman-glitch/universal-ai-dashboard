def build_semantic_model(
    df,
    semantics
):

    model = {

        "entities": {},

        "dimensions": [],

        "measures": [],

        "dates": [],

        "keys": [],

        "unknown": []
    }

    # ==============================
    # Семантические сущности
    # ==============================

    for column, role in semantics.items():

        if role not in model["entities"]:

            model["entities"][role] = []

        model["entities"][role].append(
            column
        )

    # ==============================
    # Измерения
    # ==============================

    dimension_roles = [

        "product",
        "customer",
        "department"
    ]

    for column, role in semantics.items():

        if role in dimension_roles:

            model["dimensions"].append(
                column
            )

    # ==============================
    # Показатели
    # ==============================

    measure_roles = [

        "amount",
        "quantity",
        "plan",
        "actual"
    ]

    for column, role in semantics.items():

        if role in measure_roles:

            model["measures"].append(
                column
            )

    # ==============================
    # Даты
    # ==============================

    for column, role in semantics.items():

        if role == "date":

            model["dates"].append(
                column
            )

    # ==============================
    # Потенциальные ключи
    # ==============================

    for column in df.columns:

        try:

            unique_count = (
                df[column]
                .nunique()
            )

            row_count = len(df)

            if (
                row_count > 0
                and unique_count / row_count
                > 0.90
            ):

                model["keys"].append(
                    column
                )

        except Exception:

            pass

    # ==============================
    # Неопознанные поля
    # ==============================

    for column, role in semantics.items():

        if role == "unknown":

            model["unknown"].append(
                column
            )

    return model
