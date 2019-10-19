from django.contrib import admin

from application_info.models import University, Department


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    pass


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    pass
