from app.core.unit_of_work import UnitOfWork
from app.schemas.report import DashboardReport


class ReportService:


    # ==================================================
    # DASHBOARD
    # ==================================================

    def get_dashboard(self):

        with UnitOfWork() as uow:

            data = uow.reports.get_dashboard_statistics()

            return DashboardReport(
                users=data["users"],
                products=data["products"],
                categories=data["categories"],
                orders=data["orders"],
            )