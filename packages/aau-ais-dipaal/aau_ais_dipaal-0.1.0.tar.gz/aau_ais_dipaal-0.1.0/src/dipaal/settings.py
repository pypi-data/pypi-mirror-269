from pydantic import BaseSettings, SecretStr, SettingsConfigDict


class EngineSettings(BaseSettings):

    user: str
    password: SecretStr
    host: str
    port: str
    database: str

    @property
    def url(self) -> str:
        return f'postgresql+psycopg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}'

    model_config = SettingsConfigDict(env_prefix='DIPAAL_')
