from utils.copilot_orchestrator import (
    run_copilot_analysis
)


def build_copilot_dashboard(
    df,
    semantics,
    scenario
):

    result = run_copilot_analysis(
        df=df,
        semantics=semantics,
        scenario=scenario
    )

    dashboard = {

        # ====================================
        # Паспорт данных
        # ====================================

        "data_passport": {

            "domain":
                result["domain_result"].get(
                    "domain"
                ),

            "confidence":
                result["domain_result"].get(
                    "confidence"
                ),

            "dimensions":
                len(
                    result["semantic_model"].get(
                        "dimensions",
                        []
                    )
                ),

            "measures":
                len(
                    result["semantic_model"].get(
                        "measures",
                        []
                    )
                ),

            "dates":
                len(
                    result["semantic_model"].get(
                        "dates",
                        []
                    )
                )
        },

        # ====================================
        # Семантическая модель
        # ====================================

        "semantic_model":
            result["semantic_model"],

        # ====================================
        # Объяснение домена
        # ====================================

        "domain_explanations":
            result[
                "domain_explanations"
            ],

        # ====================================
        # План анализа
        # ====================================

        "analysis_plan":
            result[
                "analysis_plan"
            ],

        # ====================================
        # Доступные анализы
        # ====================================

        "available_analyses":
            result[
                "available_analyses"
            ],

        # ====================================
        # Выполненные анализы
        # ====================================

        "analysis_results":
            result[
                "analysis_results"
            ],

        # ====================================
        # Инсайты
        # ====================================

        "model_insights":
            result[
                "model_insights"
            ],

        # ====================================
        # Copilot рекомендации
        # ====================================

        "recommendations":
            result[
                "recommendations"
            ]
    }

    return dashboard
