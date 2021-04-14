from django.contrib import admin

# Register your models here.
from .models import Project, Bugreport

admin.site.register(Project)
admin.site.register(Bugreport)

