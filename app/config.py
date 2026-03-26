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


class ShowtimesJStreamConfig(BaseModel):
    name: str = "showtimes_stream"
    subjects: list[str] = ["showtimes.>", ]
    retention: RetentionPolicy = RetentionPolicy.LIMITS
    max_age: int = 24 * 60 * 60
    discard: DiscardPolicy = DiscardPolicy.OLD


class CatalogJStreamConfig(BaseModel):
    name: str = "catalog_stream"
    subjects: list[str] = ["catalog.>", ]
    retention: RetentionPolicy = RetentionPolicy.LIMITS
    max_age: int = 24 * 60 * 60
    discard: DiscardPolicy = DiscardPolicy.OLD


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
    catalog: CatalogJStreamConfig = CatalogJStreamConfig()
    showtimes: ShowtimesJStreamConfig = ShowtimesJStreamConfig()
    nats: NatsConfig


settings = Settings()
