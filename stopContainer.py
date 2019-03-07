import docker

client = docker.from_env()

def stop_container(container):

	container.stop(timeout=3)



