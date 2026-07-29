from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


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

    customer_id: int

    username: str

    total_orders: int

    total_spent: Decimal

    average_order_value: Decimal
    
    
class LowStockReport(BaseModel):
    """
    Products with stock below the configured threshold.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    stock: int
    
    
class CategoryPerformanceReport(BaseModel):
    """
    Sales performance grouped by category.
    """

    model_config = ConfigDict(from_attributes=True)

    category_name: str
    total_sold: int
    revenue: Decimal
    
    
class DailySalesReport(BaseModel):
    """
    Daily sales analytics report.
    """

    model_config = ConfigDict(from_attributes=True)

    date: date 
    total_orders: int
    revenue: Decimal
    average_order_value: Decimal
    
    
class WeeklySalesReport(BaseModel):
    """
    Weekly sales analytics report.
    """

    model_config = ConfigDict(from_attributes=True)

    week: str
    total_orders: int
    revenue: Decimal
    average_order_value: Decimal
    
    
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