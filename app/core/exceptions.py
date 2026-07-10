class AppException(Exception):

    status_code = 500
    detail = "Internal server error"


    def __init__(
        self,
        detail: str | None = None
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

    status_code = 500
    detail = "Database error"



# =========================
# AUTH
# =========================

class AuthenticationException(AppException):

    status_code = 401
    detail = "Authentication failed"



class PermissionDeniedException(AppException):

    status_code = 403
    detail = "Permission denied"



class UsernameAlreadyExistsException(AppException):

    status_code = 400
    detail = "Username already exists"



# =========================
# USERS
# =========================

class UserNotFoundException(AppException):

    status_code = 404
    detail = "User not found"



# =========================
# PRODUCTS
# =========================

class ProductNotFoundException(AppException):

    status_code = 404
    detail = "Product not found"



class ProductInactiveException(AppException):

    status_code = 400
    detail = "Product is inactive"



class InsufficientStockException(AppException):

    status_code = 400
    detail = "Insufficient stock"



# =========================
# CATEGORIES
# =========================

class CategoryNotFoundException(AppException):

    status_code = 404
    detail = "Category not found"



# =========================
# ORDERS
# =========================

class OrderNotFoundException(AppException):

    status_code = 404
    detail = "Order not found"



# =========================
# VALIDATION
# =========================

class ValidationException(AppException):

    status_code = 422
    detail = "Validation error"
