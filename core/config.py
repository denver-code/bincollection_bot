from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str
    TOKEN: str

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
