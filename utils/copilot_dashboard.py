from utils.copilot_orchestrator import (
    run_copilot_analysis
)


def build_copilot_dashboard(
    df,
    semantics,
    scenario
):
    """
    Формирует единый объект Dashboard,
    который используется renderer-ом.
    """

    result = run_copilot_analysis(
        df=df,
        semantics=semantics,
        scenario=scenario
    )

    dashboard = {

        # ====================================
        # Исходные данные
        # ====================================

        "source_df": df,

        "semantic_model": result.get(
            "semantic_model",
            {}
        ),

        # ====================================
        # Паспорт данных
        # ====================================

        "data_passport": {

            "domain": (
                result.get(
                    "domain_result",
                    {}
                ).get(
                    "domain",
                    "Не определен"
                )
            ),

            "confidence": (
                result.get(
                    "domain_result",
                    {}
                ).get(
                    "confidence",
                    0
                )
            ),

            "dimensions": len(
                result.get(
                    "semantic_model",
                    {}
                ).get(
                    "dimensions",
                    []
                )
            ),

            "measures": len(
                result.get(
                    "semantic_model",
                    {}
                ).get(
                    "measures",
                    []
                )
            )
        },

        # ====================================
        # Объяснение домена
        # ====================================

        "domain_explanations": (
            result.get(
                "domain_result",
                {}
            ).get(
                "reasons",
                []
            )
        ),

        # ====================================
        # Инсайты модели данных
        # ====================================

        "model_insights": result.get(
            "model_insights",
            []
        ),

        # ====================================
        # Аналитика
        # ====================================

        "available_analyses": result.get(
            "available_analyses",
            []
        ),

        "analysis_plan": result.get(
            "analysis_plan",
            []
        ),

        "analysis_results": result.get(
            "analysis_results",
            []
        ),

        # ====================================
        # Рекомендации
        # ====================================

        "recommendations": result.get(
            "recommendations",
            []
        ),

        # ====================================
        # Дополнительные данные
        # ====================================

        "scenario": scenario
    }

    return dashboard
