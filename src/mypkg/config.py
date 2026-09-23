from pydantic import model_validator
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    environment: str = "local"
    port: int = 8000
    api_key: str | None = None

    @model_validator(mode="after")
    def check_production_has_key(self) -> "Settings":
        if self.environment == "production" and not self.api_key:
            raise ValueError("api_key is required when environment is in production")
        return self