from django.contrib import admin
from .models import Lesson, Course

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'duration_hours', 'price', 'has_certificate', 'status']
    list_filter = ['status', 'has_certificate']
    search_fields = ['name', 'description', 'syllabus']
    list_per_page = 10
    ordering = ['name']
    readonly_fields = ['created_at', 'updated_at']
    filter_horizontal = ['instructors']
    fieldsets = (
        ('Informações básicas', {
            'fields': ('name', 'description', 'image', 'status'),
        }),
        ('Conteúdo programático', {
            'fields': ('syllabus',),
            'description': 'Aceita Markdown (## títulos, - bullets, **negrito**).',
        }),
        ('Detalhes do curso', {
            'fields': ('duration_hours', 'price', 'min_age', 'has_certificate', 'donation_kg_required'),
        }),
        ('Equipe', {
            'fields': ('instructors',),
        }),
        ('Auditoria', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['course', 'start_date', 'start_time', 'end_time', 'capacity', 'instructor']
    list_filter = ['course', 'instructor']
    search_fields = ['course__name', 'instructor__employee__user__first_name']
    list_per_page = 10
    ordering = ['course', 'start_date']

