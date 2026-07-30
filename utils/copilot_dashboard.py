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
        # Исходный DataFrame
        # ====================================

        "source_df": df,

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

         
