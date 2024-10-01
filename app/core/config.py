from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Project"
    DESCRIPTION: str = "A FastAPI application"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"

    # Security settings
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ALGORITHM: str = "HS256"

    # Database settings
    PG_DATABASE_URL: str
    DATABASE_URL: str  # Add the field from your environment

    # OpenAI API Key (assuming you need it)
    OPENAI_API_KEY: str  # Add the field from your environment

    # CORS settings
    BACKEND_CORS_ORIGINS: list = ["*"]

    class Config:
        env_file = ".env"  # Specifies the .env file for environment variables

# Instantiate settings
settings = Settings()
