from typing import Protocol


class PostgresClient(Protocol):
    def django_settings(self, *args, **kwargs):
        raise NotImplementedError

    def sqlalchemy_engine_options(self, *args, **kwargs):
        raise NotImplementedError

    async def sqlalchemy_async_engine_options(self, *args, **kwargs):
        raise NotImplementedError

    def sqlalchemy_engine(self, *args, **kwargs):
        raise NotImplementedError

    async def sqlalchemy_async_engine(self, *args, **kwargs):
        raise NotImplementedError
