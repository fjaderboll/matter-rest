from functools import lru_cache
from pydantic import AnyUrl, Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = Field("Matter REST API", description="Display name for the service")
    server_ws_url: AnyUrl = Field(
        "ws://localhost:5580/ws", description="WebSocket endpoint for the Matter server"
    )
    request_timeout: int = Field(60, description="Timeout in seconds for Matter server calls")
    allow_origins: list[str] = Field(default_factory=lambda: ["*"])

    class Config:
        env_file = ".env"
        env_prefix = "MATTER_"
        case_sensitive = False


@lru_cache
def get_settings() -> Settings:
    return Settings()
