# Python imports
import typing

# PyPI imports
import docker

client = docker.from_env()

def get_containers(image: str) -> typing.List[docker.models.containers.Container]:
    """
    Args:
        image: example "flask"
    """
    containers_list = client.containers.list()
    containers = [
        container
        for container in containers_list
        if image in container.name
    ]
    return containers

def get_stats(container: docker.models.containers.Container) -> dict:
    stats = container.stats(stream=False)
    stats.update({'attrs': container.attrs})
    return stats