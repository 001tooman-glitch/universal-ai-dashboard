import pandas as pd

def build_kpi_report(df, kpis):

    rows = []

    for kpi in kpis:

        if kpi in df.columns:

            try:

                value = pd.to_numeric(
                    df[kpi],
                    errors="coerce"
                ).sum()

                rows.append({
                    "Показатель": kpi,
                    "Значение": value
                })

            except Exception:

                pass

    return pd.DataFrame(rows)
