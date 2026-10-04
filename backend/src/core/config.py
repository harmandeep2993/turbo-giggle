"""
Configuration settings for the Calculation API, read from environment variables.
"""

# Fixed: was "from pydantic import BaseSettings", which fails in Pydantic v2.
# BaseSettings moved to the separate pydantic-settings package.
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    App settings. Each field is read from the environment variable with the
    same name (case-insensitive), then from .env, and falls back to the default.
    """

    # Fixed: "class Config: env_file = '.env'" is Pydantic v1 style.
    # In v2 the options go in model_config.
    model_config = SettingsConfigDict(env_file=".env")

    app_name: str = "Calculation API"
    debug: bool = False
    # Fixed: renamed allowed_origin -> allowed_origins because it holds a list.
    # When set from an environment variable it must be JSON, e.g.
    # ALLOWED_ORIGINS='["http://localhost:5173"]'
    allowed_origins: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]

    tenant_id: str
    api_client_id: str
    frontend_client_id: str

    # Fixed: removed items_per_user because nothing uses it yet.


# One shared instance: settings are read once at startup and imported everywhere.
settings = Settings()

# Fixed: removed the "if __name__ == '__main__'" block. It used print() and the
# v1 method .dict(); check values with the server or a test instead.
