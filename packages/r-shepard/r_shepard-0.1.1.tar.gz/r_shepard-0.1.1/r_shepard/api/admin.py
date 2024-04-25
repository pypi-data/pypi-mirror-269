from django.contrib import admin

from .models import Container, Project

admin.site.site_header = "R-Shepard"
admin.site.site_title = "R-Shepard"
admin.site.index_title = "Admin Area"

# Register your models here.

admin.site.register(Project)
admin.site.register(Container)
