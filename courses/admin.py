from django.contrib import admin
from .models import Class, Course, Enrollment, Student


'''
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'duration', 'price', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    list_editable = ['is_active']
    list_per_page = 10
    ordering = ['name']
    readonly_fields = ['created_at', 'updated_at']
    fields = ['name', 'description', 'duration', 'price', 'is_active', 'created_at', 'updated_at']
'''

admin.site.register(Course)
admin.site.register(Class)
admin.site.register(Student)
admin.site.register(Enrollment)
