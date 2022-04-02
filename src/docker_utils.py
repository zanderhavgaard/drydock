import docker
import config
import console

console = console.default_console

# we only need a single docker client
CLIENT = docker.from_env()


def run_container(image: str) -> docker.models.containers.Container:

    # creates a list of strins without spaces
    dummy_command = "tail -f /dev/null".split(" ")

    container = CLIENT.containers.run(image, dummy_command, detach=True, remove=config.REMOVE_CONTAINER)

    return container


def stop_container(container: docker.models.containers.Container):

    # second timeout for stopping container as int
    timeout = 0

    container.stop(timeout=timeout)


def exec_in_container(container: docker.models.containers.Container, command: str):

    # turn command into a list of strings delimited at spaces
    command = command.split(" ")

    console.print("command", command)

    if config.STREAM_EXEC_OUTPUT:
        exit_code, stream = container.exec_run(command, stream=True)

        for line in stream:
            decoded = line.decode("utf-8")
            console.print(decoded, end="")

        console.print("done")

    else:
        exit_code, output = container.exec_run(command)
        output = output.decode("utf-8")
        console.print(output)

    #  print(exit_code)
    #  print(output)
