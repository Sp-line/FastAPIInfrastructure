import asyncio
from contextlib import asynccontextmanager

from nats import connect

from config import settings


@asynccontextmanager
async def nats_connection(url: str):
    nc = await connect(url)
    try:
        yield nc
    finally:
        await nc.close()


async def setup_infrastructure() -> None:
    async with nats_connection(str(settings.nats.url)) as nc:
        js = nc.jetstream()

        stream_configs = [
            settings.catalog.model_dump(),
            settings.showtimes.model_dump(),
            settings.purchases.model_dump(),
        ]

        streams = [js.add_stream(**config) for config in stream_configs]
        await asyncio.gather(*streams)


if __name__ == "__main__":
    asyncio.run(setup_infrastructure())
