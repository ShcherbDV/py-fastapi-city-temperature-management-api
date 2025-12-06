from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    PROJECT_NAME: str = 'py-fastapi-city-temperature-management-api'

    SQLITE_DATABASE_URL: str | None = "sqlite+aiosqlite:///./city_temperature.db"

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
