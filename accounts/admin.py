from django.contrib import admin

from core.admin_helpers import NativeDatePickerMixin

from .models import Instructor, Employee

@admin.register(Employee)
class EmployeeAdmin(NativeDatePickerMixin, admin.ModelAdmin):
    list_display = ['user', 'role', 'hire_date']
    search_fields = ['user__username', 'user__first_name', 'role']
    list_filter = ['role']
    list_per_page = 10

@admin.register(Instructor)
class InstrutorAdmin(admin.ModelAdmin):
    list_display = ['employee', 'specialty', 'bio']
    list_filter = ['specialty']
    search_fields = ['specialty']
    list_per_page = 10
    ordering = ['employee__user__first_name']

