from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.schemas.customer import (
    CustomerCreate,
    CustomerResponse,
    CustomerUpdate,
)
from app.services.customer_service import CustomerService
from app.core.unit_of_work import UnitOfWork


router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
)


def get_customer_service():
    uow = UnitOfWork()
    return CustomerService(uow)


@router.post(
    "",
    response_model=CustomerResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_customer(
    customer: CustomerCreate,
    service: CustomerService = Depends(get_customer_service),
):
    return service.create_customer(customer)


@router.get(
    "",
    response_model=list[CustomerResponse],
)
def get_customers(
    limit: int = 20,
    offset: int = 0,
    service: CustomerService = Depends(get_customer_service),
):
    return service.get_customers(
        limit,
        offset,
    )


@router.get(
    "/{customer_id}",
    response_model=CustomerResponse,
)
def get_customer(
    customer_id: UUID,
    service: CustomerService = Depends(get_customer_service),
):
    return service.get_customer_by_id(customer_id)


@router.put(
    "/{customer_id}",
    response_model=CustomerResponse,
)
def update_customer(
    customer_id: UUID,
    data: CustomerUpdate,
    service: CustomerService = Depends(get_customer_service),
):
    return service.update_customer(
        customer_id,
        data,
    )


@router.delete(
    "/{customer_id}",
    response_model=CustomerResponse,
)
def delete_customer(
    customer_id: UUID,
    service: CustomerService = Depends(get_customer_service),
):
    return service.delete_customer(customer_id)


@router.patch(
    "/{customer_id}/restore",
    response_model=CustomerResponse,
)
def restore_customer(
    customer_id: UUID,
    service: CustomerService = Depends(get_customer_service),
):
    return service.restore_customer(customer_id)