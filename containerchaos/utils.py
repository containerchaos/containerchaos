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

def _filter_stats(stats: dict) -> dict:
    cpu_stats_total_usage = stats['cpu_stats']['cpu_usage']['total_usage']
    memory_stats_usage = stats['memory_stats']['usage']
    created = stats['attrs']['Created']
    return {
        'cpu_stats_total_usage': cpu_stats_total_usage,
        'memory_stats_usage': memory_stats_usage,
        'created': created,
        'status': stats['attrs']['State']['Status']
    }

def get_stats(container: docker.models.containers.Container) -> dict:
    stats = container.stats(stream=False)
    stats.update({'attrs': container.attrs})
    # print(stats)
    filtered = _filter_stats(stats)
    # print(filtered)
    return filtered

def find_most_cpu(containers: list):
    largest_container = None
    largest_value = 0
    for container in containers:
        stats = get_stats(container)
        if stats['cpu_stats_total_usage'] > largest_value:
            largest_value = stats['cpu_stats_total_usage']
            largest_container = container
    return largest_container

def stop_container(container):
	container.stop(timeout=3)