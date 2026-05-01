from rest_framework import serializers
from .models import Course, Lesson

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [
            'id', 'name', 'description', 'syllabus',
            'duration_hours', 'price', 'status',
            'image', 'min_age', 'has_certificate',
            'donation_kg_required', 'instructors',
        ]

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = [
            'id', 'course', 'start_date', 'start_time', 'end_time',
            'capacity', 'instructor', 'label', 'is_private',
        ]
