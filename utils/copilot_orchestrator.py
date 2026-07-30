from utils.semantic_engine import (
    build_semantic_model
)

from utils.domain_classifier import (
    classify_domain
)

from utils.domain_explainer import (
    explain_domain
)

from utils.analysis_selector import (
    select_analyses,
    build_analysis_plan
)

from utils.analysis_executor import (
    execute_analysis
)

from utils.data_model_insights import (
    generate_data_model_insights
)

from utils.copilot_recommendation_engine import (
    build_copilot_recommendations
)


def run_copilot_analysis(
    df,
    semantics,
    scenario
):

    # ====================================
    # Семантическая модель
    # ====================================

    semantic_model = (
        build_semantic_model(
            df,
            semantics
        )
    )

    # ====================================
    # Классификация домена
    # ====================================

    domain_result = (
        classify_domain(
            semantic_model,
            scenario
        )
    )

    # ====================================
    # Объяснение домена
    # ====================================

    domain_explanations = (
        explain_domain(
            semantic_model,
            domain_result
        )
    )

    # ====================================
    # Доступные анализы
    # ====================================

    analyses = (
        select_analyses(
            semantic_model
        )
    )

    analysis_plan = (
        build_analysis_plan(
            semantic_model
        )
    )

    # ====================================
    # Выполнение анализов
    # ====================================

    analysis_results = []

    for analysis in analyses:

        result = execute_analysis(
            analysis["id"],
            df,
            semantic_model
        )

        analysis_results.append(
            result
        )

    # ====================================
    # Инсайты модели данных
    # ====================================

    model_insights = (
        generate_data_model_insights(
            semantic_model
        )
    )

    # ====================================
    # Copilot рекомендации
    # ====================================

    recommendations = (
        build_copilot_recommendations(
            domain_result=domain_result,
            semantic_model=semantic_model,
            available_analyses=analyses,
            analysis_results=analysis_results,
            insights=model_insights
        )
    )

    # ====================================
    # Финальный результат
    # ====================================

    return {

        "semantic_model":
            semantic_model,

        "domain_result":
            domain_result,

        "domain_explanations":
            domain_explanations,

        "available_analyses":
            analyses,

        "analysis_plan":
            analysis_plan,

        "analysis_results":
            analysis_results,

        "model_insights":
            model_insights,

        "recommendations":
            recommendations
    }
