from django.contrib import admin

from application_info.models import Department


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    pass
