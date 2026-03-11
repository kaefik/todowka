from fastapi import HTTPException


class NotFoundException(HTTPException):
    status_code = 404


class ValidationErrorException(HTTPException):
    status_code = 422


class ConflictException(HTTPException):
    status_code = 409


class ReminderException(HTTPException):
    status_code = 500
