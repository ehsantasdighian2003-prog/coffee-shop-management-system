class AppException(Exception):
    """
    Base application exception.
    """

    status_code: int = 500
    detail: str = "Internal server error"

    def __init__(
        self,
        detail: str | None = None,
    ):
        if detail:
            self.detail = detail

        super().__init__(
            self.detail
        )


# =========================
# DATABASE
# =========================

class DatabaseException(AppException):

    status_code: int = 500
    detail = "Database error"


# =========================
# AUTH
# =========================

class AuthenticationException(AppException):

    status_code: int = 401
    detail = "Authentication failed"


class PermissionDeniedException(AppException):

    status_code: int = 403
    detail = "Permission denied"


class UsernameAlreadyExistsException(AppException):

    status_code: int = 400
    detail = "Username already exists"


# =========================
# USERS
# =========================

class UserNotFoundException(AppException):

    status_code: int = 404
    detail = "User not found"


# =========================
# PRODUCTS
# =========================

class ProductNotFoundException(AppException):

    status_code: int = 404
    detail = "Product not found"


class ProductInactiveException(AppException):

    status_code: int = 400
    detail = "Product is inactive"


class InsufficientStockException(AppException):

    status_code: int = 400
    detail = "Insufficient stock"


# =========================
# CATEGORIES
# =========================

class CategoryNotFoundException(AppException):

    status_code: int = 404
    detail = "Category not found"


# =========================
# ORDERS
# =========================

class OrderNotFoundException(AppException):

    status_code: int = 404
    detail = "Order not found"


# =========================
# VALIDATION
# =========================

class ValidationException(AppException):

    status_code: int = 422
    detail = "Validation error"