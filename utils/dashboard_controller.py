from utils.dashboard_factory import build_dashboard
from utils.inventory_dashboard import (
    build_inventory_dashboard
)
from utils.time_series_dashboard import (
    build_time_series_dashboard
)


def build_dashboard_controller(
    df,
    domain,
    scenario,
    semantics
):

    # ====================================
    # Получаем тип дашборда
    # ====================================

    dashboard = build_dashboard(
        df=df,
        domain=domain,
        scenario=scenario,
        semantics=semantics,
        inventory_dashboard=(
            build_inventory_dashboard
        )
    )

    dashboard_name = dashboard[
        "dashboard"
    ]

    dashboard_data = dashboard[
        "data"
    ]

    # ====================================
    # Временные ряды
    # ====================================

    if (
        dashboard_name
        == "inventory_time_series"
    ):

        dashboard_data = (
            build_time_series_dashboard(
                df
            )
        )

    # ====================================
    # Результат
    # ====================================

    return {

        "dashboard_name":
            dashboard_name,

        "dashboard_data":
            dashboard_data
    }
