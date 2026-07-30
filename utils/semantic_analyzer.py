def analyze_semantics(df):

    result = {}

    for column in df.columns:

        name = str(column).lower()

        if any(x in name for x in [
            "материал",
            "номенклатура",
            "товар"
        ]):
            result[column] = "product"

        elif any(x in name for x in [
            "клиент",
            "контрагент"
        ]):
            result[column] = "customer"

        elif any(x in name for x in [
            "цех",
            "подразделение",
            "участок"
        ]):
            result[column] = "department"

        elif any(x in name for x in [
            "стоимость",
            "сумма",
            "затраты",
            "выручка"
        ]):
            result[column] = "amount"

        elif any(x in name for x in [
            "количество",
            "объем",
            "остаток"
        ]):
            result[column] = "quantity"

        elif any(x in name for x in [
            "дата",
            "период",
            "месяц"
        ]):
            result[column] = "date"

        elif any(x in name for x in [
            "план"
        ]):
            result[column] = "plan"

        elif any(x in name for x in [
            "факт"
        ]):
            result[column] = "actual"

        else:
            result[column] = "unknown"

    return result
