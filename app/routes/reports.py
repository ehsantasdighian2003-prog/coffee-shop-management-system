from fastapi import APIRouter

from app.schemas.report import (
    CategoryPerformanceReport,
    CustomerReport,
    DashboardReport,
    LowStockReport,
    MonthlySalesReport,
    SalesReport,
    TopProductReport,
    DailySalesReport,
    WeeklySalesReport,
    RevenueTrendReport,
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


@router.get(
    "/customers",
    response_model=list[CustomerReport]
)
def get_customer_report():

    return report_service.get_customer_report()


@router.get(
    "/low-stock",
    response_model=list[LowStockReport],
)
def get_low_stock_report(
    threshold: int = 10,
):

    return report_service.get_low_stock_products(
        threshold=threshold
    )
    
    
@router.get(
    "/category-performance",
    response_model=list[CategoryPerformanceReport],
)
def get_category_performance_report():

    return report_service.get_category_performance()


@router.get(
    "/daily-sales",
    response_model=list[DailySalesReport],
)
def get_daily_sales_report():

    return report_service.get_daily_sales_report()


@router.get(
    "/weekly-sales",
    response_model=list[WeeklySalesReport]
)
def get_weekly_sales_report():

    return report_service.get_weekly_sales_report()


# ==================================================
# REVENUE TREND REPORT
# ==================================================

@router.get(
    "/revenue-trend",
    response_model=list[RevenueTrendReport],
)
def get_revenue_trend():

    return report_service.get_revenue_trend()