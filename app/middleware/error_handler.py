from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.exceptions import (
    NotFoundException,
    ValidationErrorException,
    ConflictException,
    ReminderException
)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(NotFoundException)
    async def not_found_exception_handler(request: Request, exc: NotFoundException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": "NotFoundException",
                "message": str(exc.detail),
                "details": {}
            }
        )

    @app.exception_handler(ValidationErrorException)
    async def validation_exception_handler(request: Request, exc: ValidationErrorException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": "ValidationErrorException",
                "message": str(exc.detail),
                "details": {}
            }
        )

    @app.exception_handler(ConflictException)
    async def conflict_exception_handler(request: Request, exc: ConflictException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": "ConflictException",
                "message": str(exc.detail),
                "details": {}
            }
        )

    @app.exception_handler(ReminderException)
    async def reminder_exception_handler(request: Request, exc: ReminderException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": "ReminderException",
                "message": str(exc.detail),
                "details": {}
            }
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(
            status_code=500,
            content={
                "error": "InternalServerError",
                "message": str(exc),
                "details": {}
            }
        )
