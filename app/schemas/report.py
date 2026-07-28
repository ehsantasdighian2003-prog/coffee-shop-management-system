from decimal import Decimal

from pydantic import BaseModel


class DashboardReport(BaseModel):
    users: int
    products: int
    categories: int
    orders: int


class SalesReport(BaseModel):
    total_orders: int
    total_revenue: Decimal
    average_order_value: Decimal