from uuid import UUID

from app.core.exceptions import (
    CustomerAlreadyExistsException,
    CustomerNotFoundException,
)
from app.core.unit_of_work import UnitOfWork
from app.schemas.customer import (
    CustomerCreate,
    CustomerUpdate,
)


class CustomerService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def create_customer(
        self,
        customer: CustomerCreate,
    ):
        with self.uow:
            existing_customer = (
                self.uow.customer.get_customer_by_phone(
                    customer.phone
                )
            )

            if existing_customer:
                raise CustomerAlreadyExistsException()

            result = self.uow.customer.create_customer(
                customer.model_dump()
            )

            self.uow.commit()

            return result

    def get_customer_by_id(
        self,
        customer_id: UUID,
    ):
        with self.uow:
            customer = (
                self.uow.customer.get_customer_by_id(
                    customer_id
                )
            )

            if not customer:
                raise CustomerNotFoundException()

            return customer

    def get_customers(
        self,
        limit: int = 20,
        offset: int = 0,
    ):
        with self.uow:
            return self.uow.customer.get_customers(
                limit,
                offset,
            )

    def update_customer(
        self,
        customer_id: UUID,
        data: CustomerUpdate,
    ):
        with self.uow:
            customer = (
                self.uow.customer.get_customer_by_id(
                    customer_id
                )
            )

            if not customer:
                raise CustomerNotFoundException()

            result = self.uow.customer.update_customer(
                customer_id,
                data.model_dump(
                    exclude_unset=True
                ),
            )

            self.uow.commit()

            return result

    def delete_customer(
        self,
        customer_id: UUID,
    ):
        with self.uow:
            result = (
                self.uow.customer.soft_delete_customer(
                    customer_id
                )
            )

            if not result:
                raise CustomerNotFoundException()

            self.uow.commit()

            return result

    def restore_customer(
        self,
        customer_id: UUID,
    ):
        with self.uow:
            result = (
                self.uow.customer.restore_customer(
                    customer_id
                )
            )

            if not result:
                raise CustomerNotFoundException()

            self.uow.commit()

            return result