import re
import subprocess

from podman import PodmanClient

from .models import Container
from .podman import HOST_IP, PODMAN_SOCKET


def tailscale_serve(port: int, bg: bool = True, path: str = None):
    command = "tailscale serve"
    if bg:
        command += " --bg"
    if path:
        command += f" --set-path={path}"
    command += f" {port}"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    # If result.stderr contains "Tailscale is stopped", then start it
    if result.stderr and "Tailscale is stopped" in result.stderr:
        subprocess.run("tailscale up", shell=True)
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

    # Extract URL from output
    match = re.search(r"(https://\S+)", result.stdout)
    if match:
        url = match.group(1)
        print(f"Container served within tailnet at {url}")
        return url


def serve_container(container: Container):
    path = f"/{container.project.slug}/{container.container_id}"

    # Apply path to RStudio configuration
    with PodmanClient(base_url=PODMAN_SOCKET) as client:
        podman_container = client.containers.get(
            f"rstudio_{container.project.slug}_{container.container_id}"
        )
        podman_container.exec_run(
            cmd=[
                "/bin/sh",
                "-c",
                f"if ! grep -q 'www-root-path={path}' /etc/rstudio/rserver.conf; then echo 'www-root-path={path}' >> /etc/rstudio/rserver.conf; fi",
            ],
            privileged=True,
            detach=True,
        )
        podman_container.restart()

    container.tailscale_serve_url = tailscale_serve(container.port, True, path=path)
    container.local_url = ""
    container.save()


def stop_serve_container(container: Container):
    path = f"/{container.project.slug}/{container.container_id}"
    escaped_path = path.replace("/", "\\/")
    print(escaped_path)
    command = f"tailscale serve {path} off"
    subprocess.run(command, shell=True)
    with PodmanClient(base_url=PODMAN_SOCKET) as client:
        podman_container = client.containers.get(
            f"rstudio_{container.project.slug}_{container.container_id}"
        )
        podman_container.exec_run(
            cmd=[
                "/bin/sh",
                "-c",
                f"if grep -q 'www-root-path={escaped_path}' /etc/rstudio/rserver.conf; then sed -i '/www-root-path={escaped_path}/d' /etc/rstudio/rserver.conf; fi",
            ],
            privileged=True,
            detach=True,
        )
        podman_container.restart()

    container.tailscale_serve_url = ""
    container.local_url = f"http://{HOST_IP}:{container.port}"
    container.save()


def tailscale_funnel(port: int, bg: bool = True, path: str = None):
    command = "tailscale funnel"
    if bg:
        command += " --bg"
    if path:
        command += f" --set-path={path}"
    command += f" {port}"
    subprocess.run(command, shell=True)
