def detect_domain(df):

    cols = " ".join(
        [str(c).lower() for c in df.columns]
    )

    if any(x in cols for x in [
        "материал",
        "остаток",
        "склад",
        "цех"
    ]):
        return "Склад и запасы"

    if any(x in cols for x in [
        "план",
        "факт",
        "бюджет",
        "затраты"
    ]):
        return "Бюджетирование"

    if any(x in cols for x in [
        "клиент",
        "товар",
        "выручка",
        "продажи"
    ]):
        return "Продажи"

    return "Не определено"
