from pydantic import Field, PostgresDsn
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    debug: bool = Field(alias='DEBUG', default=True)

    # API URLs
    nationalize_api_url: str = Field(
        alias='NATIONALIZE_API_URL', default='https://api.nationalize.io'
    )
    rest_countries_api_url: str = Field(
        alias='REST_COUNTRIES_API_URL', default='https://restcountries.com/v3.1'
    )

    # Database settings
    postgres_user: str = Field(alias='POSTGRES_USER', default='postgres')
    postgres_password: str = Field(alias='POSTGRES_PASSWORD', default='admin')
    postgres_host: str = Field(alias='POSTGRES_HOST', default='postgres')
    postgres_port: int = Field(alias='POSTGRES_PORT', default=5432)
    postgres_db: str = Field(alias='POSTGRES_DB', default='postgres')

    @property
    def postgres_url(self) -> str:
        """Get PostgreSQL connection URL.

        Returns:
            str: PostgreSQL connection URL
        """
        return str(
            PostgresDsn.build(
                scheme='postgresql+asyncpg',
                username=self.postgres_user,
                password=self.postgres_password,
                host=self.postgres_host,
                port=5432,
                path=self.postgres_db,
            )
        )
