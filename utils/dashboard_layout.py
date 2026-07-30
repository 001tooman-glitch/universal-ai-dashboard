def get_dashboard_sections():

    return {

        # ====================================
        # Верхняя часть дашборда
        # ====================================

        "header": [

            "kpi_cards",

            "copilot_summary"
        ],

        # ====================================
        # Основная аналитика
        # ====================================

        "analytics": [

            "trend_chart",

            "top_materials",

            "abc_chart",

            "xyz_chart",

            "abc_xyz_heatmap"
        ],

        # ====================================
        # Инсайты
        # ====================================

        "insights": [

            "domain_insights",

            "model_insights",

            "copilot_recommendations"
        ],

        # ====================================
        # Детальная информация
        # ====================================

        "details": [

            "analysis_results",

            "available_analyses",

            "analysis_plan",

            "data_preview"
        ]
    }


def get_dashboard_order():

    return [

        "kpi_cards",

        "copilot_summary",

        "trend_chart",

        "top_materials",

        "abc_chart",

        "xyz_chart",

        "abc_xyz_heatmap",

        "domain_insights",

        "model_insights",

        "copilot_recommendations",

        "analysis_results",

        "available_analyses",

        "analysis_plan",

        "data_preview"
    ]


def get_compact_dashboard_order():

    return [

        "kpi_cards",

        "trend_chart",

        "top_materials",

        "abc_chart",

        "xyz_chart",

        "abc_xyz_heatmap",

        "copilot_recommendations"
    ]
