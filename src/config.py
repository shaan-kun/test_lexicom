from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env')

    host: str = 'localhost'
    port: int = 8000
    redis_host: str = 'localhost'
    redis_port: int = 6379
    cors_origins: list[str] = ['http://localhost']


settings = Settings()
