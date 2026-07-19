from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.exceptions import AppException
from app.core.logging import get_logger


logger = get_logger(__name__)


# =========================
# Custom Application Exceptions
# =========================

async def app_exception_handler(
    request: Request,
    exc: AppException
):

    logger.warning(
        f"Application error: {exc.detail} | "
        f"path={request.url.path}"
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail,
        },
    )


# =========================
# HTTP Exceptions
# =========================

async def http_exception_handler(
    request: Request,
    exc: StarletteHTTPException
):

    logger.warning(
        f"HTTP error: {exc.status_code} | "
        f"path={request.url.path}"
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail,
        },
    )


# =========================
# Request Validation Errors
# =========================

async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):

    logger.warning(
        f"Validation error | "
        f"path={request.url.path} | "
        f"errors={exc.errors()}"
    )

    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": "Validation Error",
            "errors": exc.errors(),
        },
    )


# =========================
# Global Unexpected Errors
# =========================

async def general_exception_handler(
    request: Request,
    exc: Exception
):

    print(
        "UNEXPECTED ERROR:",
        repr(exc)
    )

    logger.error(
        f"Unexpected error | "
        f"path={request.url.path} | "
        f"error={repr(exc)}",
        exc_info=True
    )

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal Server Error",
        },
    )