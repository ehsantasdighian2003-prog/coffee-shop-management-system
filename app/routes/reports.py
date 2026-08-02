from fastapi import APIRouter, Depends, Query

from app.core.security import admin_required
from app.schemas.report import (
    CategoryPerformanceReport,
    CustomerReport,
    DailySalesReport,
    DashboardReport,
    LowStockReport,
    MonthlySalesReport,
    RevenueTrendReport,
    SalesReport,
    TopProductReport,
    WeeklySalesReport,
    YearlySalesReport,
    BestSellingHour,
    ProfitReport,
    PaymentSummaryReport,
    EmployeeAnalyticsReport,
)
from app.services.report_service import ReportService


router = APIRouter(
    prefix="/reports",
    tags=["Reports"],
)


report_service = ReportService()


# ==================================================
# SALES REPORT
# ==================================================

@router.get(
    "/sales",
    response_model=SalesReport,
)
def get_sales_report(
    current_user: dict = Depends(admin_required),
):
    return report_service.get_sales_report()


# ==================================================
# DASHBOARD REPORT
# ==================================================

@router.get(
    "/dashboard",
    response_model=DashboardReport,
)
def get_dashboard_report(
    current_user: dict = Depends(admin_required),
):
    return report_service.get_dashboard_report()


# ==================================================
# TOP PRODUCTS REPORT
# ==================================================

@router.get(
    "/top-products",
    response_model=list[TopProductReport],
)
def get_top_products(
    limit: int = Query(
        default=5,
        ge=1,
        le=100,
        description="Number of top products to return",
    ),
    current_user: dict = Depends(admin_required),
):
    return report_service.get_top_products(limit)


# ==================================================
# MONTHLY SALES REPORT
# ==================================================

@router.get(
    "/monthly-sales",
    response_model=list[MonthlySalesReport],
)
def get_monthly_sales_report(
    current_user: dict = Depends(admin_required),
):
    return report_service.get_monthly_sales_report()


# ==================================================
# CUSTOMER REPORT
# ==================================================

@router.get(
    "/customers",
    response_model=list[CustomerReport],
)
def get_customer_report(
    current_user: dict = Depends(admin_required),
):
    return report_service.get_customer_report()


# ==================================================
# LOW STOCK REPORT
# ==================================================

@router.get(
    "/low-stock",
    response_model=list[LowStockReport],
)
def get_low_stock_report(
    threshold: int = Query(
        default=10,
        ge=0,
        description="Minimum stock threshold",
    ),
    current_user: dict = Depends(admin_required),
):
    return report_service.get_low_stock_products(
        threshold=threshold,
    )


# ==================================================
# CATEGORY PERFORMANCE REPORT
# ==================================================

@router.get(
    "/category-performance",
    response_model=list[CategoryPerformanceReport],
)
def get_category_performance_report(
    current_user: dict = Depends(admin_required),
):
    return report_service.get_category_performance()


# ==================================================
# DAILY SALES REPORT
# ==================================================

@router.get(
    "/daily-sales",
    response_model=list[DailySalesReport],
)
def get_daily_sales_report(
    current_user: dict = Depends(admin_required),
):
    return report_service.get_daily_sales_report()


# ==================================================
# WEEKLY SALES REPORT
# ==================================================

@router.get(
    "/weekly-sales",
    response_model=list[WeeklySalesReport],
)
def get_weekly_sales_report(
    current_user: dict = Depends(admin_required),
):
    return report_service.get_weekly_sales_report()


# ==================================================
# REVENUE TREND REPORT
# ==================================================

@router.get(
    "/revenue-trend",
    response_model=list[RevenueTrendReport],
)
def get_revenue_trend(
    current_user: dict = Depends(admin_required),
):
    return report_service.get_revenue_trend()


# ==================================================
# YEARLY SALES REPORT
# ==================================================

@router.get(
    "/yearly-sales",
    response_model=YearlySalesReport,
)
def get_yearly_sales_report(
    year: int = Query(
        ...,
        ge=2000,
        le=2100,
        description="Year for sales report",
    ),
    current_user: dict = Depends(admin_required),
):
    return report_service.get_yearly_sales_report(
        year
    )
    
    
# ==================================================
# BEST SELLING HOURS REPORT
# ==================================================

@router.get(
    "/best-selling-hours",
    response_model=list[BestSellingHour],
)
def get_best_selling_hours(
    current_user: dict = Depends(admin_required),
):
    return report_service.get_best_selling_hours()


# ==================================================
# PROFIT REPORT
# ==================================================

@router.get(
    "/profit",
    response_model=ProfitReport,
)
def get_profit_report(
    current_user: dict = Depends(admin_required),
):
    return report_service.get_profit_report()


# ==================================================
# PAYMENT ANALYTICS
# ==================================================

@router.get(
    "/payment-summary",
    response_model=PaymentSummaryReport,
)
def get_payment_summary(
    current_user: dict = Depends(admin_required),
):
    return report_service.get_payment_summary()


# ==================================================
# EMPLOYEE ANALYTICS
# ==================================================

@router.get(
    "/employees",
    response_model=list[EmployeeAnalyticsReport],
)
def employee_analytics(
    current_user = Depends(admin_required),
):

    service = ReportService()

    return service.get_employee_analytics()