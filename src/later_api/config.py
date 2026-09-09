from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str

    class Config:
        env_file = "../../.env"  # Поднимаемся на уровень выше в корневую директорию  # pyright: ignore[reportUnannotatedClassAttribute]
        env_file_encoding = "utf-8"  # pyright: ignore[reportUnannotatedClassAttribute]
        extra = "ignore"  # Игнорируем лишние поля  # pyright: ignore[reportUnannotatedClassAttribute]


settings = Settings()  # pyright: ignore[reportCallIssue]
