import pandas as pd


def build_semantic_report(df, semantics):

    rows = []

    for column in df.columns:

        rows.append({

            "Поле": column,

            "Семантика": semantics.get(
                column,
                "unknown"
            )
        })

    return pd.DataFrame(rows)
