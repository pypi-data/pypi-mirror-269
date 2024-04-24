# Handling imports and missing dependencies
try:
    import redis
except ImportError:
    redis = None

# Importing the required modules

from launchflow.aws.resource import AWSResource
from pydantic import BaseModel


def _check_installs():
    if redis is None:
        raise ImportError(
            "redis library is not installed. Please install it with `pip install redis`."
        )


# Connection information model
class ElasticacheRedisConnectionInfo(BaseModel):
    host: str
    port: int
    password: str


class ElasticacheRedis(AWSResource[ElasticacheRedisConnectionInfo]):
    """A RDS SQL Postgres resource.

    Args:
    - `name`: The name of the Cloud SQL Postgres instance.

    Example usage:
    ```python
    import launchflow as lf

    elasticache = lf.aws.ElasticacheRedis("my-redis-cluster")

    # Set a key-value pair
    client = elasticache.redis()
    client.set("my-key", "my-value")

    # Async compatible
    async_client = await elasticache.redis_async()
    await async_client.set("my-key", "my-value")
    ```
    """

    def __init__(
        self,
        name: str,
    ) -> None:
        super().__init__(
            name=name,
            product_name="aws_elasticache_redis",
            create_args={},
        )

    def django_settings(self):
        connection_info = self.connect()
        return {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": f"rediss://default:{connection_info.password}@{connection_info.host}:{connection_info.port}",
        }

    def redis(self):
        """Get a Generic Redis Client object from the redis-py library.

        **Returns**:
        - The [Generic Redis Client](https://redis-py.readthedocs.io/en/stable/connections.html#generic-client) from the redis-py library.
        """
        _check_installs()
        connection_info = self.connect()
        return redis.Redis(
            host=connection_info.host,
            port=connection_info.port,
            password=connection_info.password,
            decode_responses=True,
        )

    async def redis_async(self):
        """Get an Async Redis Client object from the redis-py library.

        **Returns**:
        - The [Async Redis Client object](https://redis-py.readthedocs.io/en/stable/connections.html#async-client) from the redis-py library.
        """
        _check_installs()
        connection_info = await self.connect_async()
        return await redis.asyncio.from_url(
            f"redis://{connection_info.host}:{connection_info.port}",
            password=connection_info.password,
            decode_responses=True,
        )
