import pandas as pd

def combine_tables(tables):

    result = []

    for table_name, df in tables.items():

        temp_df = df.copy()

        temp_df["Период"] = table_name

        result.append(temp_df)

    return pd.concat(
        result,
        ignore_index=True
    )

