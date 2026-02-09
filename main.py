"""MEDirect Edge — application entry point."""

from fastapi import FastAPI

from api.case_routes import router as case_router
from api.error_handlers import register_error_handlers
from config import Settings


def create_app(settings: Settings | None = None) -> FastAPI:
    """Create and configure the FastAPI application.

    Args:
        settings: Optional Settings override. Defaults to standard settings.

    Returns:
        A configured FastAPI application.
    """
    if settings is None:
        settings = Settings()

    app = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
    )

    app.include_router(case_router)
    register_error_handlers(app)

    return app


if __name__ == "__main__":
    import uvicorn

    _settings = Settings()
    _app = create_app(_settings)
    uvicorn.run(_app, host=_settings.host, port=_settings.port)
