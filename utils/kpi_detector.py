def detect_kpis(df):

    kpis = []

    for column in df.columns:

        name = str(column).lower()

        if any(x in name for x in [
            "стоимость",
            "сумма",
            "затраты",
            "выручка"
        ]):
            kpis.append(column)

        elif any(x in name for x in [
            "количество",
            "остаток",
            "объем"
        ]):
            kpis.append(column)

        elif any(x in name for x in [
            "план",
            "факт"
        ]):
            kpis.append(column)

    return list(set(kpis))
