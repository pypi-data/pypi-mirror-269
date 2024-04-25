from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic import DetailView, ListView, View
from two_factor.views.mixins import OTPRequiredMixin

from .models import Container, Project
from .podman import (
    PodmanError,
    is_container_running,
    remove_container,
    start_container,
    stop_container,
)
from .tailscale import serve_container, stop_serve_container


class ProjectListView(OTPRequiredMixin, ListView):
    model = Project
    template_name = "project_list.html"
    context_object_name = "projects"


class ProjectDetailView(OTPRequiredMixin, DetailView):
    model = Project
    template_name = "project_detail.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        pass

    def stop_all_project_containers(self):
        # Logic to stop all podman containers for the project
        pass

    context_object_name = "project"


class CreateContainerView(View):
    def post(self, request, *args, **kwargs):
        # Get project from URL
        project = Project.objects.get(pk=self.kwargs["project_pk"])
        # Get values from form
        password = request.POST.get("password")
        ram = int(request.POST.get("ram"))
        cpus = int(request.POST.get("cpus"))

        # Calculate total resources used by all containers of the project
        total_ram = sum(container.ram for container in project.containers.all())
        total_cpus = sum(container.cpus for container in project.containers.all())

        # Check if the project has enough resources
        if total_ram + ram > project.max_ram or total_cpus + cpus > project.max_cpus:
            messages.error(request, "Not enough resources to create a new container.")
            return HttpResponseRedirect(reverse("project_detail", args=[project.pk]))

        # Create container instance with project and password
        container = Container.objects.create(
            project=project, password=password, ram=ram, cpus=cpus
        )

        # Start podman container
        try:
            start_container(project, container, password)
            container.is_running = True
            container.save()
        except PodmanError as e:
            container.delete()
            messages.error(request, str(e))
        return HttpResponseRedirect(reverse("project_detail", args=[project.pk]))


class StartContainerView(OTPRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=kwargs["project_pk"])
        container = get_object_or_404(Container, pk=kwargs["container_pk"])
        if not is_container_running(project, container):
            start_container(project, container)
        container.is_running = True
        container.save()

        html = render_to_string("container_list.html", {"project": project})
        return HttpResponse(html)


class StopContainerView(OTPRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=kwargs["project_pk"])
        container = get_object_or_404(Container, pk=kwargs["container_pk"])
        if is_container_running(project, container):
            stop_container(project, container)
        container.is_running = False
        container.save()

        html = render_to_string("container_list.html", {"project": project})
        return HttpResponse(html)


class DeleteContainerView(OTPRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=kwargs["project_pk"])
        container = get_object_or_404(Container, pk=kwargs["container_pk"])
        if is_container_running(project, container):
            if container.tailscale_serve_url:
                stop_serve_container(container)
            remove_container(project, container)
        container.delete()

        html = render_to_string("container_list.html", {"project": project})
        return HttpResponse(html)


class ServeContainerView(OTPRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=kwargs["project_pk"])
        container = get_object_or_404(Container, pk=kwargs["container_pk"])

        if is_container_running(project, container):
            serve_container(container)

        else:
            messages.error(request, "Container is not running. Serve failed.")
            return HttpResponseRedirect(reverse("project_detail", args=[project.pk]))

        html = render_to_string("container_list.html", {"project": project})
        return HttpResponse(html)


class StopServeContainerView(OTPRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=kwargs["project_pk"])
        container = get_object_or_404(Container, pk=kwargs["container_pk"])
        if is_container_running(project, container):
            stop_serve_container(container)

        html = render_to_string("container_list.html", {"project": project})
        return HttpResponse(html)
