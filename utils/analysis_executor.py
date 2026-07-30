from utils.abc_analyzer import (
    run_abc_analysis
)

from utils.xyz_analyzer import (
    run_xyz_analysis
)

from utils.abc_xyz_matrix import (
    build_abc_xyz_matrix
)

from utils.inventory_dashboard import (
    build_inventory_dashboard
)

from utils.time_series_dashboard import (
    build_time_series_dashboard
)


def execute_analysis(
    analysis_id,
    df,
    semantic_model
):

    entities = semantic_model.get(
        "entities",
        {}
    )

    result = {
        "analysis_id": analysis_id,
        "success": False,
        "data": None,
        "message": ""
    }

    try:

        # ==========================
        # PRODUCT
        # ==========================

        product_column = None

        if "product" in entities:

            product_column = (
                entities["product"][0]
            )

        # ==========================
        # AMOUNT
        # ==========================

        amount_column = None

        if "amount" in entities:

            amount_column = (
                entities["amount"][0]
            )

        # ==========================
        # QUANTITY
        # ==========================

        quantity_column = None

        if "quantity" in entities:

            quantity_column = (
                entities["quantity"][0]
            )

        # ==========================
        # ABC
        # ==========================

        if analysis_id == "abc_analysis":

            if (
                product_column
                and amount_column
            ):

                result["data"] = (
                    run_abc_analysis(
                        df,
                        product_column,
                        amount_column
                    )
                )

                result["success"] = True

                return result

        # ==========================
        # XYZ
        # ==========================

        if analysis_id == "xyz_analysis":

            if (
                product_column
                and quantity_column
            ):

                result["data"] = (
                    run_xyz_analysis(
                        df,
                        product_column,
                        quantity_column
                    )
                )

                result["success"] = True

                return result

        # ==========================
        # ABC XYZ
        # ==========================

        if analysis_id == "abc_xyz_matrix":

            if (
                product_column
                and amount_column
                and quantity_column
            ):

                abc = run_abc_analysis(
                    df,
                    product_column,
                    amount_column
                )

                xyz = run_xyz_analysis(
                    df,
                    product_column,
                    quantity_column
                )

                matrix, summary = (
                    build_abc_xyz_matrix(
                        abc,
                        xyz,
                        product_column
                    )
                )

                result["data"] = {

                    "matrix": matrix,

                    "summary": summary
                }

                result["success"] = True

                return result

        # ==========================
        # INVENTORY
        # ==========================

        if analysis_id == "inventory_analysis":

            if (
                product_column
                and amount_column
            ):

                result["data"] = (
                    build_inventory_dashboard(
                        df,
                        product_column,
                        amount_column
                    )
                )

                result["success"] = True

                return result

        # ==========================
        # TIME SERIES
        # ==========================

        if analysis_id in [

            "trend_analysis",

            "period_comparison",

            "forecast"
        ]:

            result["data"] = (
                build_time_series_dashboard(
                    df
                )
            )

            result["success"] = True

            return result

        result["message"] = (
            "Анализ пока не реализован."
        )

        return result

    except Exception as e:

        result["message"] = str(e)

        return result


def execute_analysis_plan(
    analysis_plan,
    df,
    semantic_model
):

    results = []

    for analysis in analysis_plan:

        analysis_id = (
            analysis.get("id")
        )

        if analysis_id:

            results.append(

                execute_analysis(
                    analysis_id,
                    df,
                    semantic_model
                )

            )

    return results
