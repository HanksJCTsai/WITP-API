from django.contrib import admin
from pms_project_user.models import PmsProjectUser, PmsProjectUserLog

# Register your models here.
admin.site.register(PmsProjectUser)
admin.site.register(PmsProjectUserLog)