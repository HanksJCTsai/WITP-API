from django.contrib import admin
from pms_project.models import PmsProject, PmsProjectLog

# Register your models here.
admin.site.register(PmsProject)
admin.site.register(PmsProjectLog)