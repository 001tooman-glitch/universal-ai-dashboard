import pandas as pd


def build_data_model_report(
    semantic_model
):

    rows = []

    # ====================================
    # Dimensions
    # ====================================

    for field in semantic_model.get(
        "dimensions",
        []
    ):

        rows.append({

            "Тип": "Dimension",

            "Поле": field
        })

    # ====================================
    # Measures
    # ====================================

    for field in semantic_model.get(
        "measures",
        []
    ):

        rows.append({

            "Тип": "Measure",

            "Поле": field
        })

    # ====================================
    # Dates
    # ====================================

    for field in semantic_model.get(
        "dates",
        []
    ):

        rows.append({

            "Тип": "Date",

            "Поле": field
        })

    # ====================================
    # Keys
    # ====================================

    for field in semantic_model.get(
        "keys",
        []
    ):

        rows.append({

            "Тип": "Key",

            "Поле": field
        })

    # ====================================
    # Unknown
    # ====================================

    for field in semantic_model.get(
        "unknown",
        []
    ):

        rows.append({

            "Тип": "Unknown",

            "Поле": field
        })

    return pd.DataFrame(rows)
