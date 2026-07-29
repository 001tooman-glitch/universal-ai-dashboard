import pandas as pd

def detect_relationships(tables):

    results = []

    table_names = list(tables.keys())

    for i in range(len(table_names)):

        for j in range(i + 1, len(table_names)):

            df1 = tables[table_names[i]]
            df2 = tables[table_names[j]]

            common_columns = set(df1.columns).intersection(
                set(df2.columns)
            )

            for column in common_columns:

                results.append({
                    "Таблица 1": table_names[i],
                    "Таблица 2": table_names[j],
                    "Общее поле": column
                })

    return pd.DataFrame(results)

