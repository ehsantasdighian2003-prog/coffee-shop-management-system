from fastapi import APIRouter

from app.schemas.report import (
    SalesReport,
    DashboardReport,
    TopProductReport,
    MonthlySalesReport,
)

from app.services.report_service import ReportService


router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


report_service = ReportService()


# ==================================================
# SALES REPORT
# ==================================================

@router.get(
    "/sales",
    response_model=SalesReport
)
def get_sales_report():

    return report_service.get_sales_report()


# ==================================================
# DASHBOARD REPORT
# ==================================================

@router.get(
    "/dashboard",
    response_model=DashboardReport
)
def get_dashboard_report():

    return report_service.get_dashboard_report()


# ==================================================
# TOP PRODUCTS REPORT
# ==================================================

@router.get(
    "/top-products",
    response_model=list[TopProductReport]
)
def get_top_products(
    limit: int = 5
):

    return report_service.get_top_products(
        limit
    )
    
    
# ==================================================
# MONTHLY SALES REPORT
# ==================================================

@router.get(
    "/monthly-sales",
    response_model=list[MonthlySalesReport]
)
def get_monthly_sales_report():

    return report_service.get_monthly_sales_report()