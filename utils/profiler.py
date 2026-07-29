import pandas as pd

def build_profile(df):

    return pd.DataFrame({
        "Поле": df.columns,
        "Тип": [str(df[c].dtype) for c in df.columns],
        "Пропуски": [int(df[c].isna().sum()) for c in df.columns],
        "Уникальных": [int(df[c].nunique()) for c in df.columns]
    })
