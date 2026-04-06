from django.contrib import admin
from .models import Instructor


@admin.register(Instructor)
class InstrutorAdmin(admin.ModelAdmin):
    list_display = ['name', 'specialty', 'email', 'is_active']
    list_filter = ['is_active', 'specialty']
    search_fields = ['name', 'email', 'specialty']
    list_editable = ['is_active']
    list_per_page = 10
    ordering = ['name']

