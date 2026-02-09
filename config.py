"""Application configuration for MEDirect Edge."""

from pydantic import BaseModel


class Settings(BaseModel):
    """Application settings with sensible defaults."""

    app_name: str = "MEDirect Edge"
    api_prefix: str = "/api/v1"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000
