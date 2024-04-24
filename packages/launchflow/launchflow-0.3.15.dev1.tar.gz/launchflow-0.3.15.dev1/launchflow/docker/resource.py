from typing import Any, Dict

from launchflow.context import docker_ctx
from launchflow.resource import Resource, T


class DockerResource(Resource[T]):
    def __init__(
        self,
        name: str,
        docker_image: str,
        env_vars: Dict[str, Any] = None,
        ports: Dict[int, int] = None,
    ):
        super().__init__(name, "docker", {})
        self._docker_image = docker_image
        self._env_vars = env_vars or {}
        self._ports = ports or {}

    def connection_info(self):
        raise NotImplementedError

    def connect(self):
        """
        Synchronously connect to the resource by fetching its connection info.
        """
        connection_info = docker_ctx.get_resource_connection_info_sync(
            image_name=self._docker_image,
            resource_name=self.name,
        )
        return self._connection_type.model_validate(connection_info)

    async def connect_async(self):
        """
        Asynchronously connect to the resource by fetching its connection info.
        """
        # TODO: Make this async
        connection_info = docker_ctx.get_resource_connection_info_sync(
            image_name=self._docker_image,
            resource_name=self.name,
        )
        return self._connection_type.model_validate(connection_info)

    def create(
        self,
        *,
        project_name: str = None,
        environment_name: str = None,
        replace: bool = False,
    ):
        """
        Synchronously create the resource.
        """
        del project_name, environment_name
        return docker_ctx.create_resource_operation_sync(
            resource_type=self.__class__.__name__,
            image_name=self._docker_image,
            resource_name=self.name,
            env_vars=self._env_vars,
            ports=self._ports,
            connection_info=self.connection_info(),
            replace=replace,
        )

    async def create_async(
        self,
        *,
        project_name: str = None,
        environment_name: str = None,
        replace: bool = False,
    ):
        """
        Asynchronously create the resource.
        """
        del project_name, environment_name
        # TODO: Make this async
        return docker_ctx.create_resource_operation_sync(
            resource_type=self.__class__.__name__,
            image_name=self._docker_image,
            resource_name=self.name,
            env_vars=self._env_vars,
            ports=self._ports,
            connection_info=self.connection_info(),
            replace=replace,
        )
