from podman import PodmanClient
from podman.errors import NotFound

from .models import Container, Project

HOST_IP = "localhost"
PODMAN_SOCKET = "unix:/run/user/1000/podman/podman.sock"


# 'container' always refers to the Container model instance whereas
# 'podman_container' refers to the podman container instance


class PodmanError(Exception):
    """Base class for Podman exceptions."""

    pass


def get_podman_container(client, project, container):
    """Get the podman container if it exists, else return None."""
    try:
        return client.containers.get(f"rstudio_{project.slug}_{container.container_id}")
    except NotFound:
        return None


def start_and_save_container(podman_container, container):
    """Start the podman container and save the container details."""
    podman_container.start()
    podman_container.reload()

    if not container.tailscale_serve_url:
        container.port = podman_container.ports["8787/tcp"][0]["HostPort"]
        container.local_url = f"http://{HOST_IP}:{container.port}"
        container.save()

    print(f"Container started at {container.local_url}")


def create_container_config(project, container, password):
    """Create the container configuration. Right now, it only supports RStudio."""
    return {
        "image": "docker.io/rocker/rstudio",
        "name": f"rstudio_{project.slug}_{container.container_id}",
        "detach": True,
        "ports": {"8787/tcp": None},  # Assuming default RStudio port
        "environment": {
            "PASSWORD": password,  # Set the PASSWORD environment variable for RStudio
            "ROOT": "false",
        },
        "cpu_count": container.cpus,
        "mem_limit": f"{container.ram}g",
        "mounts": [
            {
                "type": "bind",
                "source": f"{project.workspace_path}",
                "target": f"/root/{project.slug}",
                "read_only": False,
            },
            {
                "type": "bind",
                "source": f"{project.data_path}",
                "target": "/data",
                "read_only": True,
            },
        ],
    }


def start_container(project: Project, container: Container, password: str = None):
    with PodmanClient(base_url=PODMAN_SOCKET) as client:
        podman_container = get_podman_container(client, project, container)

        if podman_container is not None:
            print("Container already exists. No need to create.")
            if podman_container.status != "running":
                print("Starting container...")
                start_and_save_container(podman_container, container)
        else:
            print("Container does not exist, creating...")
            container_config = create_container_config(project, container, password)
            try:
                podman_container = client.containers.create(**container_config)
                start_and_save_container(podman_container, container)
            except Exception as e:
                raise PodmanError(f"Failed to start container: {e}")


def stop_container(project: Project, container: Container):
    with PodmanClient(base_url=PODMAN_SOCKET) as client:
        try:
            podman_container = client.containers.get(
                f"rstudio_{project.slug}_{container.container_id}"
            )
            podman_container.stop()
        except Exception as e:
            raise PodmanError(f"Failed to stop container: {e}")


def remove_container(project: Project, container: Container):
    with PodmanClient(base_url=PODMAN_SOCKET) as client:
        try:
            podman_container = client.containers.get(
                f"rstudio_{project.slug}_{container.container_id}"
            )
            podman_container.remove(force=True)
            print("Container removed.")
        except Exception as e:
            raise PodmanError(f"Failed to remove container: {e}")


def is_container_running(project: Project, container: Container):
    with PodmanClient(base_url=PODMAN_SOCKET) as client:
        try:
            podman_container = client.containers.get(
                f"rstudio_{project.slug}_{container.container_id}"
            )
            return podman_container.status == "running"
        except Exception as e:
            raise PodmanError(f"Failed to get container status: {e}")
