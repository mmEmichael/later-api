from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str

    class Config:
        env_file = "../../.env"  # Поднимаемся на уровень выше в корневую директорию
        env_file_encoding = "utf-8"
        extra = "ignore"  # Игнорируем лишние поля


settings = Settings()
