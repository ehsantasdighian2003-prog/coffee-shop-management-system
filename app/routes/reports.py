from fastapi import APIRouter

from app.schemas.report import SalesReport
from app.services.report_service import ReportService


router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


report_service = ReportService()


@router.get(
    "/sales",
    response_model=SalesReport
)
def get_sales_report():

    return report_service.get_sales_report()