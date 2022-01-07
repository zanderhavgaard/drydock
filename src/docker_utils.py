import docker


def run_test_container():

    client = docker.from_env()

    container = client.containers.run("ubuntu", ["tail", "-f", "/dev/null"], detach=True)

    print(container)

    exit_code, output = container.exec_run("echo hello world")

    print(exit_code, output)
