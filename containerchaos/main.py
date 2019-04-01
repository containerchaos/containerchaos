import subprocess
import time
import containerchaos.measure_response_time

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
        containerchaos.measure_response_time.()



if __name__ == '__main__':
    main()