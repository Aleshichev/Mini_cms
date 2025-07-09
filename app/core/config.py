from pydantic_settings import BaseSettings
from pathlib import Path
from pydantic import BaseModel

BASE_DIR = Path(__file__).parent.parent

A = ["admin"]
AM = ["admin", "manager"]
ALL = ["admin", "manager", "back_dev", "front_dev", "tester", "designer"]
COMMANDS = ["back_dev", "front_dev", "tester", "designer"]

class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "auth" / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "auth" / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    token_location: str = "headers"
    access_token_expire_minutes: int = 5
    refresh_token_expire_days: int = 10


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

    auth_jwt: AuthJWT = AuthJWT()

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @property
    def REDIS_URL(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"
    


settings = Settings()
