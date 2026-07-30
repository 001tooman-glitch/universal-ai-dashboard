from datetime import datetime

MONTHS = {
    "январь": 1,
    "февраль": 2,
    "март": 3,
    "апрель": 4,
    "май": 5,
    "июнь": 6,
    "июль": 7,
    "август": 8,
    "сентябрь": 9,
    "октябрь": 10,
    "ноябрь": 11,
    "декабрь": 12
}

def period_to_date(period):

    month_name, year = period.lower().split()

    year = int(year)

    if year < 100:
        year += 2000

    month = MONTHS[month_name]

    return datetime(year, month, 1)
