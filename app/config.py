from nats.js.api import (
    RetentionPolicy,
    DiscardPolicy
)
from pydantic import (
    BaseModel,
    NatsDsn
)
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict
)


class JStreamBaseConfig(BaseModel):
    retention: RetentionPolicy = RetentionPolicy.LIMITS
    max_age: int = 24 * 60 * 60
    discard: DiscardPolicy = DiscardPolicy.OLD


class ShowtimesConfig(JStreamBaseConfig):
    name: str = "showtimes_stream"
    subjects: list[str] = ["showtimes.>", ]


class CatalogConfig(JStreamBaseConfig):
    name: str = "catalog_stream"
    subjects: list[str] = ["catalog.>", ]


class PurchasesConfig(JStreamBaseConfig):
    name: str = "purchases_stream"
    subjects: list[str] = ["purchases.>", ]


class NatsConfig(BaseModel):
    url: NatsDsn


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env.template", ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
        extra="ignore"
    )
    catalog: CatalogConfig = CatalogConfig()
    showtimes: ShowtimesConfig = ShowtimesConfig()
    purchases: PurchasesConfig = PurchasesConfig()
    nats: NatsConfig


settings = Settings()
