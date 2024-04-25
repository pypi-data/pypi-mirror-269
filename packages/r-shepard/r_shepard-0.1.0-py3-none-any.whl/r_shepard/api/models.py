import random
import re
import string

from django.contrib.auth.hashers import check_password, make_password
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

# Create your models here.


def validate_git_url(value):
    pattern = r"(git@|http:\/\/|https:\/\/)([\w\.@:]+)(\/|:)([\w\.\/\-]+\.git)"
    if not re.match(pattern, value):
        raise ValidationError(f"{value} is not a valid Git URL")


class Project(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        help_text="The name of the project.",
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        help_text="A URL-safe slug for the project.",
    )
    data_path = models.CharField(
        max_length=1024,
        help_text="Filesystem path where project data is stored. Containers have read access here.",
    )
    workspace_path = models.CharField(
        max_length=1024,
        help_text="Filesystem path where R scripts are stored. The containers have write access here.",
    )
    max_containers = models.PositiveIntegerField(
        default=4,
        help_text="Maximum number of containers that can be run for the project.",
    )
    max_ram = models.PositiveIntegerField(
        default=32,
        help_text="Maximum amount of RAM in GB allocated for the project.",
    )
    max_cpus = models.PositiveIntegerField(
        default=8,
        help_text="Maximum number of CPUs allocated to the project.",
    )
    auto_commit_enabled = models.BooleanField(
        default=False,
        help_text="Whether automatic commits are enabled for the workspace_path.",
    )
    git_repo_url = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        validators=[validate_git_url],
        help_text="URL of the Git repository.",
    )
    commit_interval = models.PositiveIntegerField(
        default=15, help_text="Commit interval in minutes."
    )
    last_commit_time = models.DateTimeField(
        default=timezone.now,
        help_text="Last time the project was committed to the Git repository.",
    )

    # Generate a URL-safe slug for the project
    def generate_slug(self):
        """Generate a URL-safe slug from the project name."""
        return self.name.lower().replace(" ", "_")

    def running_containers(self):
        return self.containers.filter(is_running=True)

    def __str__(self):
        return self.name


class Container(models.Model):
    class Meta:
        unique_together = ("project", "container_id")

    def generate_container_id():
        """Generate a random 8-char string."""
        return "".join(random.choices(string.ascii_lowercase + string.digits, k=8))

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="containers",
        help_text="The project to which this container belongs.",
    )
    image = models.CharField(
        default="rocker/rstudio",
        max_length=255,
        help_text="The name of the container image.",
    )
    tag = models.CharField(
        default="latest",
        max_length=255,
        help_text="The tag of the container image.",
    )
    password = models.CharField(
        max_length=255,
        help_text="Password for the RStudio Rocker container.",
    )
    container_id = models.CharField(
        max_length=8,
        default=generate_container_id,
        help_text="The unique identifier of the container within the project.",
    )
    ram = models.PositiveIntegerField(
        default=2,
        help_text="Amount of RAM in GB allocated for the container.",
    )
    cpus = models.PositiveIntegerField(
        default=2,
        help_text="Number of CPUs allocated to the container.",
    )
    port = models.PositiveIntegerField(
        default=8787,
        help_text="The host port on which the container's RStudio instance is accessible.",
    )
    local_url = models.URLField(
        default="",
        max_length=1024,
        help_text="Local URL to access this container's RStudio instance",
    )
    tailscale_funnel_url = models.URLField(
        default="",
        max_length=1024,
        help_text="Tailscale Funnel URL to access this container's RStudio instance from the web",
    )
    tailscale_serve_url = models.URLField(
        default="",
        null=True,
        max_length=1024,
        help_text="Tailscale Serve URL to access this container's RStudio instance from the tailnet",
    )
    is_running = models.BooleanField(
        default=False,
        help_text="Indicates whether the container is running",
    )

    def save(self, *args, **kwargs):
        if not check_password(self.password, self.__original_password):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_password = self.password

    def __str__(self):
        return self.container_id
