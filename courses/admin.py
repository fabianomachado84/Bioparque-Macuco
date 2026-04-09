from django.contrib import admin
from .models import Lesson, Course

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'duration_hours', 'price', 'status']
    list_filter = ['status']
    search_fields = ['name', 'description']
    list_per_page = 10
    ordering = ['name']
    readonly_fields = ['created_at', 'updated_at']
    fields = ['name', 'description', 'duration_hours', 'price', 'status', 'created_at', 'updated_at']

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['course', 'start_date', 'start_time', 'end_time', 'capacity', 'instructor']
    list_filter = ['course', 'instructor']
    search_fields = ['course__name', 'instructor__employee__user__first_name']
    list_per_page = 10
    ordering = ['course', 'start_date']
    fields = ['course', 'start_date', 'start_time', 'end_time', 'capacity', 'instructor', 'created_at', 'updated_at']

