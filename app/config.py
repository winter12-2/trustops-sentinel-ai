from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --- Application Configuration ---
    app_name: str = Field(default="TrustOps Sentinel AI", alias="APP_NAME")
    app_env: str = Field(default="development", alias="APP_ENV")
    app_host: str = Field(default="127.0.0.1", alias="APP_HOST")
    app_port: int = Field(default=8000, alias="APP_PORT")
    app_debug: bool = Field(default=True, alias="APP_DEBUG")

    # --- Redis Configuration ---
    redis_host: str = Field(default="localhost", alias="REDIS_HOST")
    redis_port: int = Field(default=6379, alias="REDIS_PORT")
    redis_db: int = Field(default=0, alias="REDIS_DB")
    redis_url: str = Field(default="redis://localhost:6379/0", alias="REDIS_URL")

    # --- External APIs ---
    tavily_api_key: str = Field(default="", alias="TAVILY_API_KEY")
    watsonx_api_key: str = Field(default="", alias="WATSONX_API_KEY")
    watsonx_project_id: str = Field(default="", alias="WATSONX_PROJECT_ID")
    watsonx_url: str = Field(default="", alias="WATSONX_URL")

    # --- Database Configuration ---
    mysql_host: str = Field(default="localhost", alias="MYSQL_HOST")
    mysql_port: int = Field(default=3306, alias="MYSQL_PORT")
    mysql_user: str = Field(default="root", alias="MYSQL_USER")
    mysql_password: str = Field(default="", alias="MYSQL_PASSWORD")
    mysql_database: str = Field(default="trustops_ai", alias="MYSQL_DATABASE")

    # --- Algorand Configuration ---
    algorand_algod_address: str = Field(
        default="https://testnet-api.algonode.cloud",
        alias="ALGORAND_ALGOD_ADDRESS",
    )
    algorand_algod_token: str = Field(default="", alias="ALGORAND_ALGOD_TOKEN")
    algorand_address: str = Field(default="", alias="ALGORAND_ADDRESS")
    algorand_mnemonic: str = Field(default="", alias="ALGORAND_MNEMONIC")
    algorand_enabled: bool = Field(default=True, alias="ALGORAND_ENABLED")

    # --- Helpers ---
    def is_algorand_configured(self) -> bool:
        return bool(self.algorand_address and self.algorand_mnemonic)


settings = Settings()

