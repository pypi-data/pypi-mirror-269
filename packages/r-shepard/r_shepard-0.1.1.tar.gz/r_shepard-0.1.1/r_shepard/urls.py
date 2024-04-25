"""
URL configuration for r_shepard project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView
from two_factor.admin import AdminSiteOTPRequired
from two_factor.urls import urlpatterns as tf_urls

from r_shepard.api.views import (
    CreateContainerView,
    DeleteContainerView,
    ProjectDetailView,
    ProjectListView,
    ServeContainerView,
    StartContainerView,
    StopContainerView,
    StopServeContainerView,
)

admin.site.__class__ = AdminSiteOTPRequired

urlpatterns = [
    # Auth
    path("", include(tf_urls)),
    # Redirect empty path to /projects
    path("", RedirectView.as_view(url="/projects", permanent=True)),
    # Admin site
    path("admin/", admin.site.urls),
    # Project views
    path("projects/", ProjectListView.as_view(), name="project_list"),
    path("projects/<int:pk>/", ProjectDetailView.as_view(), name="project_detail"),
    # Container views
    path(
        "projects/<int:project_pk>/containers/new/",
        CreateContainerView.as_view(),
        name="create_container",
    ),
    path(
        "projects/<int:project_pk>/containers/<int:container_pk>/start/",
        StartContainerView.as_view(),
        name="start_container",
    ),
    path(
        "projects/<int:project_pk>/containers/<int:container_pk>/stop/",
        StopContainerView.as_view(),
        name="stop_container",
    ),
    path(
        "projects/<int:project_pk>/containers/<int:container_pk>/delete/",
        DeleteContainerView.as_view(),
        name="delete_container",
    ),
    path(
        "projects/<int:project_pk>/containers/<int:container_pk>/serve/",
        ServeContainerView.as_view(),
        name="serve_container",
    ),
    path(
        "projects/<int:project_pk>/containers/<int:container_pk>/serve/stop",
        StopServeContainerView.as_view(),
        name="stop_serve_container",
    ),
]
