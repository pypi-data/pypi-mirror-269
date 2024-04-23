try:
    import asyncpg
except ImportError:
    asyncpg = None

try:
    import pg8000
except ImportError:
    pg8000 = None

try:
    import psycopg2
except ImportError:
    psycopg2 = None

try:
    from sqlalchemy.ext.asyncio import create_async_engine
except ImportError:
    async_sessionmaker = None
    create_async_engine = None

try:
    from sqlalchemy import create_engine
except ImportError:
    create_engine = None
    DeclarativeBase = None
    sessionmaker = None

import socket

from launchflow.docker.resource import DockerResource
from pydantic import BaseModel


class DockerPostgresConnectionInfo(BaseModel):
    password: str
    postgres_port: str


def _find_open_port(start_port: int = 5432, max_checks: int = 20) -> int:
    """Find an open port starting from a given port.

    Args:
    - `start_port`: The port to start searching from.

    Returns:
    - The first open port found.
    """

    for _ in range(max_checks):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("localhost", start_port))
                return start_port
            except OSError:
                start_port += 1

    raise ValueError(f"Could not find an open port after {max_checks} checks.")


class DockerPostgres(DockerResource[DockerPostgresConnectionInfo]):
    def __init__(self, name: str, *, password: str = "password") -> None:
        """A Postgres resource running in a Docker container.

        **Arguments**:
        - `name` (str): The name of the Postgres resource. This must be globally unique.
        - `password` (str): The password for the Postgres DB. If not provided, a random password will be generated.

        **Example usage**:
        ```python
        from sqlalchemy import text
        import launchflow as lf

        postgres = lf.docker.Postgres("postgres-db")
        engine = postgres.sqlalchemy_engine()

        with engine.connect() as connection:
            print(connection.execute(text("SELECT 1")).fetchone())  # prints (1,)
        ```
        """
        self.password = password

        self.port = _find_open_port()

        super().__init__(
            name=name,
            env_vars={
                "POSTGRES_PASSWORD": self.password,
                "POSTGRES_DB": "postgres",
                "POSTGRES_USER": "postgres",
            },
            ports={"5432/tcp": self.port},
            docker_image="postgres",
        )

    def connection_info(self) -> DockerPostgresConnectionInfo:
        return DockerPostgresConnectionInfo(
            password=self.password,
            postgres_port=str(self.port),
        )

    def django_settings(self):
        if psycopg2 is None:
            raise ImportError(
                "psycopg2 is not installed. Please install it with `pip install psycopg2`."
            )

        connection_info = self.connect()
        return {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": "postgres",
            "USER": "postgres",
            "PASSWORD": connection_info.password,
            "HOST": "localhost",
            "PORT": connection_info.postgres_port,
        }

    def sqlalchemy_engine_options(self):
        if pg8000 is None:
            raise ImportError(
                "pg8000 is not installed. Please install it with `pip install pg8000`."
            )

        connection_info = self.connect()
        return {
            "url": f"postgresql+pg8000://postgres:{connection_info.password}@localhost:{connection_info.postgres_port}/postgres",
        }

    async def sqlalchemy_async_engine_options(self):
        if asyncpg is None:
            raise ImportError(
                "asyncpg is not installed. Please install it with `pip install asyncpg`."
            )

        connection_info = await self.connect_async()
        return {
            "url": f"postgresql+asyncpg://postgres:{connection_info.password}@localhost:{connection_info.postgres_port}/postgres"
        }

    def sqlalchemy_engine(self, **engine_kwargs):
        """Returns a SQLAlchemy engine for connecting to a postgres instance hosted on Docker.

        Args:
        - `**engine_kwargs`: Additional keyword arguments to pass to `sqlalchemy.create_engine`.

        Example usage:
        ```python
        import launchflow as lf
        db = lf.docker.Postgres("my-pg-db")
        engine = db.sqlalchemy_engine()
        ```
        """
        if create_engine is None:
            raise ImportError(
                "SQLAlchemy is not installed. Please install it with "
                "`pip install sqlalchemy`."
            )

        engine_options = self.sqlalchemy_engine_options()
        engine_options.update(engine_kwargs)

        return create_engine(**engine_options)

    async def sqlalchemy_async_engine(self, **engine_kwargs):
        """Returns an async SQLAlchemy engine for connecting to a postgres instance hosted on Docker.

        Args:
        - `**engine_kwargs`: Additional keyword arguments to pass to `create_async_engine`.

        Example usage:
        ```python
        import launchflow as lf
        db = lf.docker.Postgres("my-pg-db")
        engine = await db.sqlalchemy_async_engine()
        ```
        """
        if create_async_engine is None:
            raise ImportError(
                "SQLAlchemy asyncio extension is not installed. "
                "Please install it with `pip install sqlalchemy[asyncio]`."
            )

        engine_options = await self.sqlalchemy_async_engine_options()
        engine_options.update(engine_kwargs)

        return create_async_engine(**engine_options)
