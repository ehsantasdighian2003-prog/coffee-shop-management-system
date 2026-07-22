from typing import Any

from app.core.exceptions import (
    AuthenticationException,
    UserNotFoundException,
)

from app.core.security import (
    hash_password,
    verify_password,
)

from app.core.unit_of_work import UnitOfWork



class UserService:
    """
    Handles business logic related to users.
    """


    # ==================================================
    # GET USER BY ID
    # ==================================================


    def get_user_by_id(
        self,
        user_id: int,
    ) -> dict[str, Any]:


        with UnitOfWork() as uow:

            user = uow.users.get_by_id(
                user_id
            )


            if not user:

                raise UserNotFoundException()


            return user



    # ==================================================
    # GET USERS PAGINATED
    # ==================================================


    def get_users(
        self,
        limit: int = 20,
        offset: int = 0,
    ) -> dict[str, Any]:


        with UnitOfWork() as uow:

            users = uow.users.get_all(
                limit,
                offset,
            )


            total = uow.users.count_users()


            return {
                "data": users,

                "meta": {
                    "page": (offset // limit) + 1,
                    "limit": limit,
                    "total": total,
                    "pages": (
                        total + limit - 1
                    ) // limit,
                },
            }



    # ==================================================
    # UPDATE PROFILE
    # ==================================================


    def update_profile(
        self,
        user_id: int,
        user_data,
    ) -> dict[str, Any]:


        with UnitOfWork() as uow:


            user = uow.users.update_user(
                user_id,
                user_data.first_name,
                user_data.last_name,
                user_data.email,
                user_data.phone_number,
                user_data.profile_image,
            )


            if not user:

                raise UserNotFoundException()


            return user



    # ==================================================
    # CHANGE PASSWORD
    # ==================================================


    def change_password(
        self,
        user_id: int,
        old_password: str,
        new_password: str,
    ) -> dict[str, Any]:


        with UnitOfWork() as uow:


            user = uow.users.get_by_id(
                user_id
            )


            if not user:

                raise UserNotFoundException()



            if not verify_password(
                old_password,
                user["password"],
            ):

                raise AuthenticationException(
                    "Old password is incorrect"
                )



            new_hash = hash_password(
                new_password
            )


            return uow.users.update_password(
                user_id,
                new_hash,
            )



    # ==================================================
    # UPDATE ROLE
    # ==================================================


    def update_role(
        self,
        user_id: int,
        role: str,
    ) -> dict[str, Any]:


        with UnitOfWork() as uow:


            user = uow.users.update_role(
                user_id,
                role,
            )


            if not user:

                raise UserNotFoundException()


            return user



    # ==================================================
    # ACTIVATE USER
    # ==================================================


    def activate_user(
        self,
        user_id: int,
    ) -> dict[str, Any]:


        with UnitOfWork() as uow:


            user = uow.users.activate_user(
                user_id
            )


            if not user:

                raise UserNotFoundException()


            return user



    # ==================================================
    # DEACTIVATE USER
    # ==================================================


    def deactivate_user(
        self,
        user_id: int,
    ) -> dict[str, Any]:


        with UnitOfWork() as uow:


            user = uow.users.deactivate_user(
                user_id
            )


            if not user:

                raise UserNotFoundException()


            return user



    # ==================================================
    # SOFT DELETE USER
    # ==================================================


    def delete_user(
        self,
        user_id: int,
    ) -> dict[str, Any]:


        with UnitOfWork() as uow:


            user = uow.users.soft_delete_user(
                user_id
            )


            if not user:

                raise UserNotFoundException()


            return user



    # ==================================================
    # RESTORE USER
    # ==================================================


    def restore_user(
        self,
        user_id: int,
    ) -> dict[str, Any]:


        with UnitOfWork() as uow:


            user = uow.users.restore_user(
                user_id
            )


            if not user:

                raise UserNotFoundException()


            return user