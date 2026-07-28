from fastapi import APIRouter

from app.schemas.report import DashboardReport
from app.services.report_service import ReportService


router = APIRouter(
    prefix="/reports",
    tags=["Reports"],
)


report_service = ReportService()


@router.get(
    "/dashboard",
    response_model=DashboardReport,
)
def get_dashboard():

    return report_service.get_dashboard()