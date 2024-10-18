from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://quizdb:quizdb@localhost/quizdb"
    redis_url: str = "redis://localhost:6379/0"
    broker_url: str = "redis://localhost:6379/0"
    result_backend_url: str = "redis://localhost:6379/0"

    class Config:
        env_file = ".env"


settings = Settings()
