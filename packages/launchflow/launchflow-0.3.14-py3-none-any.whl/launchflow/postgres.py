from typing import Dict, Optional

from launchflow.gcp.compute_engine import ComputeEnginePostgres
from launchflow.postgres_client import PostgresClient


# TODO: Implement a generic Postgres class that acts like a router for the various
# PostgresClient implementations. This class is not used yet.
class Postgres:
    _resource_routes: Dict[str, PostgresClient]

    def register(self, environment_name: str, client: PostgresClient):
        self._resource_routes[environment_name] = client

    def get_client(self, environment_name: str) -> Optional[PostgresClient]:
        return self._resource_routes.get(environment_name)


if __name__ == "__main__":
    postgres = Postgres()
    postgres.register("dev", ComputeEnginePostgres("postgres"))
