def get_analysis_catalog():

    return {

        # ====================================
        # Универсальные анализы
        # ====================================

        "basic_statistics": {

            "name": "Базовая статистика",

            "required_entities": [],

            "description":
                "Общая статистика по данным"
        },

        "top_analysis": {

            "name": "ТОП-анализ",

            "required_entities": [
                "amount"
            ],

            "description":
                "Рейтинг объектов по показателям"
        },

        # ====================================
        # Временные ряды
        # ====================================

        "trend_analysis": {

            "name": "Анализ трендов",

            "required_entities": [
                "date",
                "amount"
            ],

            "description":
                "Анализ изменения показателей во времени"
        },

        "period_comparison": {

            "name": "Сравнение периодов",

            "required_entities": [
                "date",
                "amount"
            ],

            "description":
                "Сравнение выбранных периодов"
        },

        "forecast": {

            "name": "Прогнозирование",

            "required_entities": [
                "date",
                "amount"
            ],

            "description":
                "Построение прогнозов"
        },

        # ====================================
        # Склад
        # ====================================

        "abc_analysis": {

            "name": "ABC-анализ",

            "required_entities": [
                "product",
                "amount"
            ],

            "description":
                "Классификация объектов по вкладу в стоимость"
        },

        "xyz_analysis": {

            "name": "XYZ-анализ",

            "required_entities": [
                "product",
                "quantity"
            ],

            "description":
                "Классификация объектов по стабильности потребления"
        },

        "abc_xyz_matrix": {

            "name": "Матрица ABC/XYZ",

            "required_entities": [
                "product",
                "amount",
                "quantity"
            ],

            "description":
                "Комбинированный ABC/XYZ анализ"
        },

        "inventory_analysis": {

            "name": "Анализ запасов",

            "required_entities": [
                "product",
                "quantity"
            ],

            "description":
                "Анализ остатков и запасов"
        },

        # ====================================
        # Продажи
        # ====================================

        "sales_analysis": {

            "name": "Анализ продаж",

            "required_entities": [
                "customer",
                "amount"
            ],

            "description":
                "Анализ продаж по клиентам"
        },

        "customer_analysis": {

            "name": "Анализ клиентов",

            "required_entities": [
                "customer"
            ],

            "description":
                "Исследование клиентской базы"
        },

        "product_analysis": {

            "name": "Анализ товаров",

            "required_entities": [
                "product",
                "amount"
            ],

            "description":
                "Исследование продуктового портфеля"
        },

        # ====================================
        # Бюджетирование
        # ====================================

        "plan_fact_analysis": {

            "name": "План-Факт анализ",

            "required_entities": [
                "plan",
                "actual"
            ],

            "description":
                "Сравнение плановых и фактических данных"
        },

        "variance_analysis": {

            "name": "Анализ отклонений",

            "required_entities": [
                "plan",
                "actual"
            ],

            "description":
                "Расчет отклонений и причин"
        }
    }


def get_available_analyses(
    semantic_model
):

    entities = set(
        semantic_model.get(
            "entities",
            {}
        ).keys()
    )

    catalog = get_analysis_catalog()

    available = []

    for analysis_id, analysis in catalog.items():

        required = set(
            analysis[
                "required_entities"
            ]
        )

        if required.issubset(
            entities
        ):

            available.append({

                "id": analysis_id,

                "name":
                    analysis["name"],

                "description":
                    analysis["description"]
            })

    return available
