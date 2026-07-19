from app.core.unit_of_work import UnitOfWork
from app.core.security import pwd_context, verify_password

from app.core.exceptions import (
    UserNotFoundException,
)


class UserService:


    # =========================
    # GET USER BY ID
    # =========================

    def get_user_by_id(
        self,
        user_id: int
    ):

        with UnitOfWork() as uow:

            user = uow.users.get_by_id(
                uow.conn,
                user_id
            )

            if not user:
                raise UserNotFoundException()

            return user


    # =========================
    # GET ALL USERS
    # =========================

    def get_users(
        self,
        limit: int = 20,
        offset: int = 0
    ):

        with UnitOfWork() as uow:

            users = uow.users.get_all(
                uow.conn,
                limit,
                offset
            )

            total = uow.users.count_users(
                uow.conn
            )

            return {
                "users": users,
                "total": total,
                "page": (offset // limit) + 1,
                "limit": limit
            }


    # =========================
    # UPDATE PROFILE
    # =========================

    def update_profile(
        self,
        user_id: int,
        user_data
    ):

        with UnitOfWork() as uow:

            user = uow.users.update_user(
                uow.conn,
                user_id,
                user_data.first_name,
                user_data.last_name,
                user_data.email,
                user_data.phone_number,
                user_data.profile_image
            )

            if not user:
                raise UserNotFoundException()

            return user


    # =========================
    # CHANGE PASSWORD
    # =========================

    def change_password(
        self,
        user_id: int,
        old_password: str,
        new_password: str
    ):

        with UnitOfWork() as uow:

            user = uow.users.get_by_id(
                uow.conn,
                user_id
            )

            if not user:
                raise UserNotFoundException()


            if not verify_password(
                old_password,
                user["password"]
            ):
                raise Exception(
                    "Old password is incorrect"
                )


            hashed_password = pwd_context.hash(
                new_password
            )


            return uow.users.update_password(
                uow.conn,
                user_id,
                hashed_password
            )


    # =========================
    # UPDATE ROLE
    # =========================

    def update_role(
        self,
        user_id: int,
        role: str
    ):

        with UnitOfWork() as uow:

            user = uow.users.update_role(
                uow.conn,
                user_id,
                role
            )

            if not user:
                raise UserNotFoundException()

            return user


    # =========================
    # ACTIVATE USER
    # =========================

    def activate_user(
        self,
        user_id: int
    ):

        with UnitOfWork() as uow:

            return uow.users.activate_user(
                uow.conn,
                user_id
            )


    # =========================
    # DEACTIVATE USER
    # =========================

    def deactivate_user(
        self,
        user_id: int
    ):

        with UnitOfWork() as uow:

            return uow.users.deactivate_user(
                uow.conn,
                user_id
            )


    # =========================
    # DELETE USER
    # =========================

    def delete_user(
        self,
        user_id: int
    ):

        with UnitOfWork() as uow:

            return uow.users.soft_delete_user(
                uow.conn,
                user_id
            )


    # =========================
    # RESTORE USER
    # =========================

    def restore_user(
        self,
        user_id: int
    ):

        with UnitOfWork() as uow:

            return uow.users.restore_user(
                uow.conn,
                user_id
            )