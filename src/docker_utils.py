import docker
import config
import console

console = console.default_console

# we only need a single docker client
CLIENT = docker.from_env()


def run_container(image: str) -> docker.models.containers.Container:

    pull_image(image)

    # transform string to a list of strings with no spaces
    dummy_command = "tail -f /dev/null".split(" ")

    console.print(f"Creating container ...")
    docker_container = CLIENT.containers.run(image, dummy_command, detach=True, remove=config.REMOVE_CONTAINER)
    console.print(f"Container name: {docker_container.name}")
    console.print(f"Container ID: {docker_container.id}")

    return docker_container


def pull_image(image: str):
    # there is probably an easier way to check if the image exists locally...
    found = list(filter(lambda img: image in img.tags, CLIENT.images.list()))

    if not found:
        console.print(f"Could not find image {image} locally.")
        with console.status("Pulling image ..."):
            CLIENT.images.pull(image)


def stop_container(docker_container: docker.models.containers.Container):

    # second timeout for stopping container as int
    timeout = 0

    console.print(f"Stopping container {docker_container.name} - {docker_container.id}")
    docker_container.stop(timeout=timeout)
    console.print(f"Container stopped.")


def exec_in_container(container: docker.models.containers.Container, command: str):

    # turn command into a list of strings delimited at spaces
    command_list = command.split(" ")

    with console.status(f"Running command: {command} ..."):
        if config.STREAM_EXEC_OUTPUT:
            exit_code, stream = container.exec_run(command_list, stream=True)

            console.print("Container exec output:")
            console.print("----------------------")

            for line in stream:
                decoded = line.decode("utf-8")
                print(decoded, end="")

        else:
            exit_code, output = container.exec_run(command_list)
            output = output.decode("utf-8")

            console.print("Container exec output:")
            console.print("----------------------")
            console.print(output)
