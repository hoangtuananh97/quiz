from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://quizdb:quizdb@localhost/quizdb"
    redis_url: str = "redis://localhost:6379/0"
    broker_url: str = "redis://localhost:6379/0"
    result_backend_url: str = "redis://localhost:6379/0"
    max_client: int = 50
    score: int = 10

    class Config:
        env_file = ".env"


settings = Settings()
