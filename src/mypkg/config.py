from pydantic import Field, SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Typed application configuration, read from the environment."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    environment: str = "local"
    port: int = 8000

    hf_token: SecretStr | None = Field(
        default=None,
        description="Hugging Face User Access Token (if using gated/private models)",
    )

    model_name: str = Field(
        default="all-MiniLM-L6-v2",
        description="Hugging Face model repository or identifier",
    )

    @model_validator(mode="after")
    def check_production_has_key(self) -> "Settings":
        if self.environment == "production" and not self.hf_token:
            raise ValueError("hf_token is required when environment is in production")
        return self
