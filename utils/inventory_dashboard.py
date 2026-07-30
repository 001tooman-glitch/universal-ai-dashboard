from utils.abc_analyzer import run_abc_analysis
from utils.xyz_analyzer import run_xyz_analysis
from utils.abc_xyz_matrix import build_abc_xyz_matrix
from utils.abc_xyz_insights import generate_abc_xyz_insights


def build_inventory_dashboard(
    df,
    product_column,
    amount_column
):

    result = {}

    # ====================================
    # ABC
    # ====================================

    abc_df = run_abc_analysis(
        df,
        product_column,
        amount_column
    )

    # ====================================
    # XYZ
    # ====================================

    xyz_df = run_xyz_analysis(
        df,
        product_column,
        amount_column
    )

    # ====================================
    # ABC/XYZ Matrix
    # ====================================

    matrix_df, summary_df = (
        build_abc_xyz_matrix(
            abc_df,
            xyz_df,
            product_column
        )
    )

    # ====================================
    # Insights
    # ====================================

    insights = (
        generate_abc_xyz_insights(
            matrix_df,
            summary_df
        )
    )

    # ====================================
    # Result
    # ====================================

    result["abc"] = abc_df

    result["xyz"] = xyz_df

    result["matrix"] = matrix_df

    result["summary"] = summary_df

    result["insights"] = insights

    return result
