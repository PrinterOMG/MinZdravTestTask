from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix='',
        case_sensitive=False,
        env_file='.env',
        env_file_encoding='utf-8'
    )

    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_host: str = 'postgres'
    postgres_port: int = 5432

    users_service_url: str

    database_url: str = ''

    def __init__(self):
        super().__init__()
        self.database_url = f'postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}'


settings = Settings()
