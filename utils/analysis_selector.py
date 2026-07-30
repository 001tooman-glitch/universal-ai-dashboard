from utils.analysis_catalog import (
    get_available_analyses
)


def select_analyses(
    semantic_model,
    max_items=10
):

    available = get_available_analyses(
        semantic_model
    )

    priority_order = [

        # Склад

        "abc_xyz_matrix",
        "abc_analysis",
        "xyz_analysis",
        "inventory_analysis",

        # Временные ряды

        "trend_analysis",
        "period_comparison",
        "forecast",

        # Продажи

        "sales_analysis",
        "customer_analysis",
        "product_analysis",

        # План-Факт

        "plan_fact_analysis",
        "variance_analysis",

        # Универсальные

        "top_analysis",
        "basic_statistics"
    ]

    priority_map = {

        analysis_id: index

        for index, analysis_id

        in enumerate(priority_order)
    }

    for analysis in available:

        analysis["priority"] = (
            priority_map.get(
                analysis["id"],
                999
            )
        )

    selected = sorted(
        available,
        key=lambda x: x["priority"]
    )

    return selected[:max_items]


def get_primary_analysis(
    semantic_model
):

    analyses = select_analyses(
        semantic_model,
        max_items=1
    )

    if analyses:

        return analyses[0]

    return None


def build_analysis_plan(
    semantic_model
):

    analyses = select_analyses(
        semantic_model
    )

    plan = []

    for position, analysis in enumerate(
        analyses,
        start=1
    ):

        plan.append({

            "Шаг": position,

            "Анализ": analysis["name"],

            "Описание": analysis[
                "description"
            ]
        })

    return plan
