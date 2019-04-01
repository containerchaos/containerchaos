import containerchaos.utils

def test_container_utils():
    containers = containerchaos.utils.get_containers("flaskapp")
    assert isinstance(containers, list)
    assert len(containers) >= 1

    stat = containerchaos.utils.get_stats(containers[0])
    assert isinstance(stat, dict)
    # print(stat)

    for c in containers:
        print(containerchaos.utils.get_stats(c))