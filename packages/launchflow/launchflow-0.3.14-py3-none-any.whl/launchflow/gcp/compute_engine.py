# Handling imports and missing dependencies
try:
    import redis
except ImportError:
    redis = None
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


from copy import deepcopy
from typing import Any, Dict, List, Optional

from launchflow.gcp.resource import GCPResource
from launchflow.resource import T
from launchflow.utils import generate_random_password
from pydantic import BaseModel


def _check_redis_installs():
    if redis is None:
        raise ImportError(
            "redis library is not installed. Please install it with `pip install redis`."
        )


class ComputeEngineBaseConnectionInfo(BaseModel):
    """
    Every Compute Engine resource has some common attributes as well as additional outputs that are resource-specific.
    """

    vm_ip: str
    ports: List[int]


class ComputeEngineRedisConnectionInfo(ComputeEngineBaseConnectionInfo):
    password: str
    redis_port: str


class ComputeEnginePostgresConnectionInfo(ComputeEngineBaseConnectionInfo):
    password: str
    postgres_port: str


class DockerConfig(BaseModel):
    image: str
    args: List[str]
    environment_variables: Dict[str, str]


class FirewallConfig(BaseModel):
    expose_ports: List[int]


class VMConfig(BaseModel):
    additional_outputs: Dict[str, str]
    docker_cfg: DockerConfig
    firewall_cfg: Optional[FirewallConfig] = None


class ComputeEngine(GCPResource[T]):
    def __init__(self, name: str, vm_config: VMConfig) -> None:
        """Generic compute engine resource.

        **Arguments**:
        - `name` (str): The name of the resource. This must be globally unique.
        - `vm_config` (VMConfig): The configuration for the VM.
        """
        super().__init__(
            name=name,
            product_name="gcp_compute_engine",
            create_args=vm_config.model_dump(mode="json"),
        )


class ComputeEnginePostgres(ComputeEngine[ComputeEnginePostgresConnectionInfo]):
    def __init__(self, name: str, *, password: Optional[str] = None) -> None:
        """A Postgres resource running on a VM in Google Compute Engine.

        **Arguments**:
        - `name` (str): The name of the Postgres VM resource. This must be globally unique.
        - `password` (str): The password for the Postgres DB. If not provided, a random password will be generated.

        **Example usage**:
        ```python
        from sqlalchemy import text
        import launchflow as lf

        postgres_compute_engine = lf.gcp.ComputeEnginePostgres("ce-postgres-mn-test-2")
        engine = postgres_compute_engine.sqlalchemy_engine()

        with engine.connect() as connection:
            print(connection.execute(text("SELECT 1")).fetchone())  # prints (1,)
        ```
        """
        if password is None:
            password = generate_random_password()
        super().__init__(
            name=name,
            vm_config=VMConfig(
                additional_outputs={"postgres_port": "5432", "password": password},
                docker_cfg=DockerConfig(
                    image="postgres:latest",
                    args=[],
                    environment_variables={"POSTGRES_PASSWORD": password},
                ),
                firewall_cfg=FirewallConfig(expose_ports=[5432]),
            ),
        )

    def _create_args_eq(self, other_args: Dict[str, Any]) -> bool:
        """Custom comparison function for create args.

        We generate the postgres DB password in the resource so we can pass along the environment variables
        which needs to be set in the VMConfig. This means that two equivalent instances of the resource will
        never have the same create args. This is an equality function that handles this.

        **Arguments**:
        - `other_args` (dict): The other create args to compare against.

        **Returns**:
        - True if the create args are equivalent, False otherwise.
        """
        own_args = deepcopy(self._create_args)
        other_args = deepcopy(other_args)

        try:
            del own_args["additional_outputs"]["password"]
            del other_args["additional_outputs"]["password"]

            del own_args["docker_cfg"]["environment_variables"]["POSTGRES_PASSWORD"]
            del other_args["docker_cfg"]["environment_variables"]["POSTGRES_PASSWORD"]
        except KeyError:
            return False

        return own_args == other_args

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
            "HOST": connection_info.vm_ip,
            "PORT": connection_info.postgres_port,
        }

    def sqlalchemy_engine_options(self):
        if pg8000 is None:
            raise ImportError(
                "pg8000 is not installed. Please install it with `pip install pg8000`."
            )

        connection_info = self.connect()
        return {
            "url": f"postgresql+pg8000://postgres:{connection_info.password}@{connection_info.vm_ip}:{connection_info.postgres_port}/postgres",
        }

    async def sqlalchemy_async_engine_options(self):
        if asyncpg is None:
            raise ImportError(
                "asyncpg is not installed. Please install it with `pip install asyncpg`."
            )

        connection_info = await self.connect_async()
        return {
            "url": f"postgresql+asyncpg://postgres:{connection_info.password}@{connection_info.vm_ip}:{connection_info.postgres_port}/postgres"
        }

    def sqlalchemy_engine(self, **engine_kwargs):
        """Returns a SQLAlchemy engine for connecting to a postgres instance hosted on GCP compute engine.

        Args:
        - `**engine_kwargs`: Additional keyword arguments to pass to `sqlalchemy.create_engine`.

        Example usage:
        ```python
        import launchflow as lf
        db = lf.gcp.ComputeEnginePostgres("my-pg-db")
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
        """Returns an async SQLAlchemy engine for connecting to a postgres instance hosted on GCP compute engine.

        Args:
        - `**engine_kwargs`: Additional keyword arguments to pass to `create_async_engine`.

        Example usage:
        ```python
        import launchflow as lf
        db = lf.gcp.ComputeEnginePostgres("my-pg-db")
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


class ComputeEngineRedis(ComputeEngine[ComputeEngineRedisConnectionInfo]):
    """A Redis resource running on a VM in Google Compute Engine.

    **Attributes**:
    - `name` (str): The name of the Redis VM resource. This must be globally unique.
    - `password` (str): The password for the Redis DB. If not provided, a random password will be generated.

    Example usage:
    ```python
    import launchflow as lf

    redis = lf.gcp.ComputeEngineRedis("my-redis-instance")

    # Set a key-value pair
    client = redis.redis()
    client.set("my-key", "my-value")

    # Async compatible
    async_client = await redis.redis_async()
    await async_client.set("my-key", "my-value")
    ```
    """

    def __init__(self, name: str, *, password: Optional[str] = None) -> None:
        if password is None:
            password = generate_random_password()
        super().__init__(
            name=name,
            vm_config=VMConfig(
                additional_outputs={"redis_port": "6379", "password": password},
                docker_cfg=DockerConfig(
                    image="redis:latest",
                    args=f"redis-server --appendonly yes --requirepass {password}".split(),
                    environment_variables={},
                ),
                firewall_cfg=FirewallConfig(expose_ports=[6379]),
            ),
        )

        self._async_pool = None
        self._sync_client = None

    def django_settings(self):
        connection_info = self.connect()
        return {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": f"redis://default:{connection_info.password}@{connection_info.vm_ip}:{connection_info.redis_port}",
        }

    def _create_args_eq(self, other_args: Dict[str, Any]) -> bool:
        """Custom comparison function for create args.

        We generate the password in the resource so we can pass it along in the startup command
        which needs to be set in the VMConfig. This means that two equivalent instances of the resource will
        never have the same create args. This is an equality function that handles this.

        **Arguments**:
        - `other_args` (dict): The other create args to compare against.

        **Returns**:
        - True if the create args are equivalent, False otherwise.
        """
        own_args = deepcopy(self._create_args)
        other_args = deepcopy(other_args)

        try:
            del own_args["additional_outputs"]["password"]
            del other_args["additional_outputs"]["password"]

            own_args["docker_cfg"]["args"].pop()
            other_args["docker_cfg"]["args"].pop()
        except KeyError:
            return False

        return own_args == other_args

    def redis(self, *, decode_responses: bool = True):
        """Get a Generic Redis Client object from the redis-py library.

        **Returns**:
        - The [Generic Redis Client](https://redis-py.readthedocs.io/en/stable/connections.html#generic-client) from the redis-py library.
        """
        _check_redis_installs()
        connection_info = self.connect()
        if self._sync_client is None:
            self._sync_client = redis.Redis(
                host=connection_info.vm_ip,
                port=int(connection_info.redis_port),
                password=connection_info.password,
                decode_responses=decode_responses,
            )
        return self._sync_client

    async def redis_async(self, *, decode_responses: bool = True):
        """Get an Async Redis Client object from the redis-py library.

        **Returns**:
        - The [Async Redis Client object](https://redis-py.readthedocs.io/en/stable/connections.html#async-client) from the redis-py library.
        """
        _check_redis_installs()
        connection_info = await self.connect_async()
        if self._async_pool is None:
            self._async_pool = await redis.asyncio.from_url(
                f"redis://{connection_info.vm_ip}:{connection_info.redis_port}",
                password=connection_info.password,
                decode_responses=decode_responses,
            )
        return self._async_pool
