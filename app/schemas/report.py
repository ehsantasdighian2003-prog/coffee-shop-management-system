from pydantic import BaseModel


class DashboardReport(BaseModel):
    users: int
    products: int
    categories: int
    orders: int