from collections.abc import Generator

from app.core.unit_of_work import UnitOfWork


def get_uow() -> Generator[UnitOfWork, None, None]:
    """
    FastAPI dependency for UnitOfWork lifecycle management.
    """

    with UnitOfWork() as uow:
        yield uow