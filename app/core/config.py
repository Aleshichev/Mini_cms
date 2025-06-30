from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str
    POSTGRES_USER: str 
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    POSTGRES_PORT: str
    POSTGRES_DB: str 
    REDIS_HOST: str
    REDIS_PORT: int
    class Config:
        env_file = ".env"
        
    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )



settings = Settings()
