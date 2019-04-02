import subprocess
import time
import measure_response_time
import utils

URL = "http://localhost/"

def _run(cmd: str):
    print("Running cmd: {}".format(cmd))
    print(subprocess.run(cmd, shell=True, capture_output=True, cwd="../docker-nginx-flask-redis-postgres/"))

def _sleep(t: int = 5):
    print("Sleeping {}s".format(t))
    time.sleep(t)

def _cleanup():
    print("Cleaning up old containers if they exist")
    _run("docker stack rm webapp")
    _run("docker-compose down")

def _setup():
    print("Setting up swarm")
    _run("docker-compose up -d")
    _run("docker-compose down")
    _run("docker swarm init")

def _deploy():
    print("Deploying to swarm")
    _run("docker stack deploy --compose-file docker-compose.yml webapp")

def main():
    _cleanup()
    _setup()

    _deploy()

    for i in range(100):
        measure_response_time.measure_response_time(URL, "Baseline")
    _cleanup()

    _deploy()
    print("Redo baseline, but dont save to csv") # To establish some API use
    for i in range(100):
        measure_response_time.measure_response_time(URL, "Baseline", write=False)
    print("By CPU Usage")
    containers = utils.get_containers("flaskapp")
    c = utils.find_most_cpu(containers)
    print("Stopping container {}".format(c))
    utils.stop_container(c)
    for i in range(100):
        measure_response_time.measure_response_time(URL, "CPU Usage")
    _cleanup()

if __name__ == '__main__':
    main()