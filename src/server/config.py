# Using python-decouple package
# from decouple import config as decouple_config, RepositoryEnv


# DATABASE_URL = decouple_config("DATABASE_URL", default="")

# Using pydantic_settings package
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


Config = Settings()
