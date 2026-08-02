from datetime import date, datetime
from decimal import Decimal

from pydantic import (
    BaseModel,
    ConfigDict,
    field_serializer,
)


# =====================================================
# SALES REPORT
# =====================================================


class SalesReport(BaseModel):
    """
    Sales statistics report schema.
    """

    model_config = ConfigDict(
        from_attributes=True
    )

    total_orders: int
    total_revenue: Decimal
    average_order_value: Decimal


# =====================================================
# DASHBOARD REPORT
# =====================================================


class DashboardReport(BaseModel):
    """
    Main dashboard statistics schema.
    """

    model_config = ConfigDict(
        from_attributes=True
    )

    users: int
    products: int
    categories: int
    orders: int

    total_revenue: Decimal
    average_order_value: Decimal


# =====================================================
# TOP PRODUCTS REPORT
# =====================================================


class TopProductReport(BaseModel):
    """
    Top selling products report schema.
    """

    model_config = ConfigDict(
        from_attributes=True
    )

    product_name: str
    total_sold: int
    revenue: Decimal


# =====================================================
# MONTHLY SALES REPORT
# =====================================================


class MonthlySalesReport(BaseModel):
    """
    Monthly sales report schema.
    """

    model_config = ConfigDict(
        from_attributes=True
    )

    month: str
    total_orders: int
    revenue: Decimal


# ==================================================
# CUSTOMER ANALYTICS REPORT
# ==================================================


class CustomerReport(BaseModel):
    """
    Customer analytics report schema.
    """

    model_config = ConfigDict(
        from_attributes=True
    )

    customer_id: int
    username: str
    total_orders: int
    total_spent: Decimal
    average_order_value: Decimal


# ==================================================
# LOW STOCK REPORT
# ==================================================


class LowStockReport(BaseModel):
    """
    Products with stock below configured threshold.
    """

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    name: str
    stock: int


# ==================================================
# CATEGORY PERFORMANCE REPORT
# ==================================================


class CategoryPerformanceReport(BaseModel):
    """
    Sales performance grouped by category.
    """

    model_config = ConfigDict(
        from_attributes=True
    )

    category_name: str
    total_sold: int
    revenue: Decimal


# ==================================================
# DAILY SALES REPORT
# ==================================================


class DailySalesReport(BaseModel):
    """
    Daily sales analytics report.
    """

    model_config = ConfigDict(
        from_attributes=True
    )

    date: date
    total_orders: int
    revenue: Decimal
    average_order_value: Decimal


# ==================================================
# WEEKLY SALES REPORT
# ==================================================


class WeeklySalesReport(BaseModel):
    """
    Weekly sales analytics report.
    """

    model_config = ConfigDict(
        from_attributes=True
    )

    week: str
    total_orders: int
    revenue: Decimal
    average_order_value: Decimal


# ==================================================
# REVENUE TREND REPORT
# ==================================================


class RevenueTrendReport(BaseModel):
    """
    Revenue trend analytics report.
    """

    model_config = ConfigDict(
        from_attributes=True
    )

    date: date
    total_orders: int
    revenue: Decimal


# ==================================================
# YEARLY SALES REPORT
# ==================================================


class YearlyMonthlySales(BaseModel):
    """
    Monthly breakdown inside yearly sales report.
    """

    model_config = ConfigDict(
        from_attributes=True
    )

    month: int
    total_orders: int
    revenue: Decimal



class YearlySalesReport(BaseModel):
    """
    Yearly sales analytics report schema.
    """

    model_config = ConfigDict(
        from_attributes=True
    )

    year: int
    total_orders: int
    total_revenue: Decimal
    monthly_sales: list[YearlyMonthlySales]
    
    
# ==================================================
# BEST SELLING HOURS REPORT
# ==================================================


class BestSellingHour(BaseModel):
    """
    Best selling hour analytics schema.
    """

    model_config = ConfigDict(
        from_attributes=True
    )

    hour: int
    total_orders: int
    revenue: Decimal

    @field_serializer("revenue")
    def serialize_revenue(
        self,
        value: Decimal,
    ):
        return str(value)


class BestSellingHoursReport(BaseModel):
    """
    Best selling hours response schema.
    """

    data: list[BestSellingHour]
    
    
# ==================================================
# PROFIT REPORT
# ==================================================

class ProfitProductReport(BaseModel):
    """
    Product profit analytics schema.
    """

    model_config = ConfigDict(
        from_attributes=True
    )

    product_name: str
    total_sold: int
    revenue: Decimal
    cost: Decimal
    profit: Decimal

    @field_serializer(
        "revenue",
        "cost",
        "profit",
    )
    def serialize_decimal(
        self,
        value: Decimal,
    ):
        return str(value)


class ProfitReport(BaseModel):
    """
    Profit report response schema.
    """

    model_config = ConfigDict(
        from_attributes=True
    )

    total_revenue: Decimal
    total_cost: Decimal
    total_profit: Decimal

    products: list[ProfitProductReport]

    @field_serializer(
        "total_revenue",
        "total_cost",
        "total_profit",
    )
    def serialize_decimal(
        self,
        value: Decimal,
    ):
        return str(value)
    
    
# ==================================================
# PAYMENT ANALYTICS
# ==================================================


class PaymentMethodStats(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    method: str
    transactions: int
    revenue: Decimal
    percentage: float

    @field_serializer("revenue")
    def serialize_revenue(
        self,
        value: Decimal,
    ):
        return str(value)


class PaymentSummaryReport(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    total_transactions: int
    total_revenue: Decimal
    methods: list[PaymentMethodStats]

    @field_serializer("total_revenue")
    def serialize_total_revenue(
        self,
        value: Decimal,
    ):
        return str(value)


class PaymentTransaction(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    order_id: int
    user_id: int
    payment_method: str
    total_price: Decimal
    created_at: datetime

    @field_serializer("total_price")
    def serialize_total_price(
        self,
        value: Decimal,
    ):
        return str(value)


class PaginatedPaymentTransactions(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    page: int
    limit: int
    total: int
    pages: int
    data: list[PaymentTransaction]
    
    
# ==================================================
# EMPLOYEE ANALYTICS
# ==================================================

class EmployeeAnalyticsReport(BaseModel):
    """
    Employee performance analytics schema.
    """

    model_config = ConfigDict(
        from_attributes=True
    )

    employee_id: int
    username: str
    total_orders: int
    total_sales: Decimal
    average_order_value: Decimal

    @field_serializer(
        "total_sales",
        "average_order_value",
    )
    def serialize_decimal(
        self,
        value: Decimal,
    ):
        return str(value)