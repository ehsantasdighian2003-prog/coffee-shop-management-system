from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class SalesReport(BaseModel):
    """
    Sales report response schema.
    """

    model_config = ConfigDict(
        from_attributes=True
    )

    total_orders: int
    total_revenue: Decimal
    average_order_value: Decimal


class DashboardReport(BaseModel):
    """
    Dashboard statistics response schema.
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