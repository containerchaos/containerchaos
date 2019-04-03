# containerchaos

```
git clone --recursive
cd containerchaos/docker-nginx-flask-redis-postgres
docker-compose up
```
Let it build and (importantly) tag your local images.
Then, once its running:
```
Ctrl+C
```

Switch to swarm mode:
```
docker swarm init
docker stack deploy --compose-file docker-compose.yml webapp
```


To cleanup:
```
docker stack rm webapp
```

## Tests

Install pipenv

```
pipenv run python -m pytest -s
```

You should see something like below for the running flask containers:
```
pipenv run python -m pytest -s                   [11:30:07]
================================================ test session starts =================================================
platform darwin -- Python 3.6.5, pytest-4.3.0, py-1.8.0, pluggy-0.9.0
rootdir: /Users/kevin/dev/containerchaos, inifile:
collected 1 item

tests/test_utils.py {<Container: 4beb6d34b4>: {'cpu_stats_total_usage': 45199380600, 'memory_stats_usage': 271527936, 'created': '2019-04-01T15:21:18.6797227Z', 'status': 'running'}}
{<Container: 33513bfac1>: {'cpu_stats_total_usage': 45177323100, 'memory_stats_usage': 273313792, 'created': '2019-04-01T15:21:18.6080046Z', 'status': 'running'}}
{<Container: 10e6bcbf1e>: {'cpu_stats_total_usage': 45118897300, 'memory_stats_usage': 273371136, 'created': '2019-04-01T15:21:18.5860682Z', 'status': 'running'}}
{<Container: 7e89d268f1>: {'cpu_stats_total_usage': 49410251400, 'memory_stats_usage': 269684736, 'created': '2019-04-01T15:20:50.1684941Z', 'status': 'running'}}
```


## To recreate the results
We didn't get around to finishing the automated script for running it all, but you can get an idea of how we gathered the data by looking at the uncompleted containerchaos/main.py script.
Instead, we did it manually by:
1. Start a Docker Swarm
2. Run the Baseline requests (`curl http://localhost/` or the GCloud IP address) and write response times to a .csv
3. Shutdown the Swarm
4. Start a new Swarm
5. Run the Baseline, but don't write out - this establishes some use on the api
6. Run `python -m pytest -s`, pick the container with the metric we're using
7. Shutdown the container by running `docker stop {containerid}`, the swarm will then autocreate a new container to maintain the specified number of replicas
8. Run the same curl request, and save the result under the specified critera (for example: "CPU Usage")
9. Repeat 3-9 for each criteria ("CPU Usage", "Memory Usage", "Uptime")
10. Repeat all of the above for the complex task by sending a request (`curl http://localhost/recurisvefib` - note the typo got shipped)

