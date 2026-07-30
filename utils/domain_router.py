def route_analysis(domain, scenario):

    if scenario == "time_series":

        return {
            "dashboard": "time_series",
            "analyses": [
                "Динамика",
                "Сравнение периодов",
                "Тренды",
                "Прогноз"
            ]
        }

    if domain == "Склад и запасы":

        return {
            "dashboard": "inventory",
            "analyses": [
                "ABC-анализ",
                "XYZ-анализ",
                "Неликвиды",
                "Анализ остатков"
            ]
        }

    if domain == "Продажи":

        return {
            "dashboard": "sales",
            "analyses": [
                "ABC клиентов",
                "ABC товаров",
                "Сезонность",
                "RFM"
            ]
        }

    if domain == "Бюджетирование":

        return {
            "dashboard": "budget",
            "analyses": [
                "План-Факт",
                "Отклонения",
                "Исполнение бюджета"
            ]
        }

    return {
        "dashboard": "generic",
        "analyses": [
            "Статистика",
            "ТОП-анализ",
            "Корреляции"
        ]
    }
