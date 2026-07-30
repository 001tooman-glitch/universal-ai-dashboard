from utils.semantic_engine import (
    build_semantic_model
)

from utils.data_model_report import (
    build_data_model_report
)

from utils.data_model_insights import (
    generate_data_model_insights
)

from utils.data_model_visualizer import (
    build_data_model_visualization
)


def build_data_model_dashboard(
    df,
    semantics
):

    semantic_model = (
        build_semantic_model(
            df,
            semantics
        )
    )

    report = (
        build_data_model_report(
            semantic_model
        )
    )

    insights = (
        generate_data_model_insights(
            semantic_model
        )
    )

    visualization = (
        build_data_model_visualization(
            semantic_model
        )
    )

    return {

        "semantic_model":
            semantic_model,

        "report":
            report,

        "insights":
            insights,

        "visualization":
            visualization
    }
