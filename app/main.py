from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.config import settings
from app.core.exceptions import AppException
from app.core.handlers import (
    app_exception_handler,
    general_exception_handler,
    http_exception_handler,
    validation_exception_handler,
)
from app.core.logging import (
    get_logger,
    setup_logging,
)

from app.routes import users
from app.routes.auth import router as auth_router
from app.routes.categories import router as categories_router
from app.routes.inventory import router as inventory_router
from app.routes.orders import router as orders_router
from app.routes.products import router as products_router
from app.routes.reports import router as reports_router


# =====================================================
# LOGGING
# =====================================================

setup_logging()

logger = get_logger(__name__)


# =====================================================
# APPLICATION LIFECYCLE
# =====================================================


@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info("Coffee Shop API started successfully")

    yield

    logger.info("Coffee Shop API shutting down")


# =====================================================
# FASTAPI APPLICATION
# =====================================================

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="Production-like Coffee Shop Management System API",
    lifespan=lifespan,
)


# =====================================================
# CORS
# =====================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =====================================================
# EXCEPTION HANDLERS
# =====================================================

app.add_exception_handler(
    AppException,
    app_exception_handler,
)

app.add_exception_handler(
    StarletteHTTPException,
    http_exception_handler,
)

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler,
)

app.add_exception_handler(
    Exception,
    general_exception_handler,
)


# =====================================================
# ROUTERS
# =====================================================

app.include_router(auth_router)

app.include_router(users.router)

app.include_router(categories_router)

app.include_router(products_router)

app.include_router(orders_router)

app.include_router(reports_router)

app.include_router(inventory_router)


# =====================================================
# ROOT
# =====================================================


@app.get("/")
def root():

    logger.info("Root endpoint accessed")

    return {
        "success": True,
        "message": "Coffee Shop API is running 🚀",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
    }


# =====================================================
# HEALTH CHECK
# =====================================================


@app.get("/health")
def health_check():

    return {
        "status": "ok",
        "service": settings.APP_NAME,
        "version": "1.0.0",
    }