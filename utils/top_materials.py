import pandas as pd


def build_top_materials(
    df,
    semantic_model,
    top_n=20
):
    """
    Формирует ТОП материалов
    по общей стоимости.
    """

    entities = semantic_model.get(
        "entities",
        {}
    )

    if "product" not in entities:

        return None

    if "amount" not in entities:

        return None

    try:

        product_column = (
            entities["product"][0]
        )

        amount_column = (
            entities["amount"][0]
        )

        result = (
            df.groupby(product_column)[amount_column]
            .sum()
            .reset_index()
            .sort_values(
                amount_column,
                ascending=False
            )
            .head(top_n)
        )

        return result

    except Exception:

        return None
