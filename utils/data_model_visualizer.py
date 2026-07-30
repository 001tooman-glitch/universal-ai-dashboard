import pandas as pd


def build_data_model_visualization(
    semantic_model
):

    nodes = []

    relations = []

    # ====================================
    # Центральная сущность
    # ====================================

    nodes.append({
        "Узел": "DATA_MODEL",
        "Тип": "ROOT"
    })

    # ====================================
    # Dimensions
    # ====================================

    for field in semantic_model.get(
        "dimensions",
        []
    ):

        nodes.append({
            "Узел": field,
            "Тип": "DIMENSION"
        })

        relations.append({
            "Источник": "DATA_MODEL",
            "Приемник": field,
            "Связь": "dimension"
        })

    # ====================================
    # Measures
    # ====================================

    for field in semantic_model.get(
        "measures",
        []
    ):

        nodes.append({
            "Узел": field,
            "Тип": "MEASURE"
        })

        relations.append({
            "Источник": "DATA_MODEL",
            "Приемник": field,
            "Связь": "measure"
        })

    # ====================================
    # Dates
    # ====================================

    for field in semantic_model.get(
        "dates",
        []
    ):

        nodes.append({
            "Узел": field,
            "Тип": "DATE"
        })

        relations.append({
            "Источник": "DATA_MODEL",
            "Приемник": field,
            "Связь": "date"
        })

    # ====================================
    # Keys
    # ====================================

    for field in semantic_model.get(
        "keys",
        []
    ):

        nodes.append({
            "Узел": field,
            "Тип": "KEY"
        })

        relations.append({
            "Источник": "DATA_MODEL",
            "Приемник": field,
            "Связь": "key"
        })

    # ====================================
    # Unknown
    # ====================================

    for field in semantic_model.get(
        "unknown",
        []
    ):

        nodes.append({
            "Узел": field,
            "Тип": "UNKNOWN"
        })

        relations.append({
            "Источник": "DATA_MODEL",
            "Приемник": field,
            "Связь": "unknown"
        })

    return {
        "nodes": pd.DataFrame(nodes),
        "relations": pd.DataFrame(relations)
    }
