"""Global exception handlers mapping domain exceptions to HTTP responses."""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from exceptions import (
    InvalidStateError,
    MEDirectError,
    NotFoundError,
    ValidationError,
)


def register_error_handlers(app: FastAPI) -> None:
    """Register global exception handlers on the FastAPI app.

    Args:
        app: The FastAPI application instance.
    """

    @app.exception_handler(NotFoundError)
    async def not_found_handler(request: Request, exc: NotFoundError) -> JSONResponse:
        """Handle NotFoundError as 404."""
        return JSONResponse(
            status_code=404,
            content={"detail": exc.message},
        )

    @app.exception_handler(InvalidStateError)
    async def invalid_state_handler(
        request: Request, exc: InvalidStateError
    ) -> JSONResponse:
        """Handle InvalidStateError as 409 Conflict."""
        return JSONResponse(
            status_code=409,
            content={"detail": exc.message},
        )

    @app.exception_handler(ValidationError)
    async def validation_handler(
        request: Request, exc: ValidationError
    ) -> JSONResponse:
        """Handle ValidationError as 422."""
        return JSONResponse(
            status_code=422,
            content={"detail": exc.message},
        )

    @app.exception_handler(MEDirectError)
    async def generic_domain_handler(
        request: Request, exc: MEDirectError
    ) -> JSONResponse:
        """Handle any other domain error as 500."""
        return JSONResponse(
            status_code=500,
            content={"detail": "An internal error occurred"},
        )
