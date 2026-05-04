from rest_framework import serializers

from accounts.serializers import InstructorPublicSerializer

from .models import Course, Lesson


class NextLessonSerializer(serializers.ModelSerializer):
    """Compact Lesson view used inside CourseSerializer.next_lesson."""

    class Meta:
        model = Lesson
        fields = ['id', 'start_date', 'start_time', 'end_time', 'capacity']


class CourseSerializer(serializers.ModelSerializer):
    instructors = InstructorPublicSerializer(many=True, read_only=True)
    next_lesson = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            'id', 'name', 'description', 'syllabus',
            'duration_hours', 'price', 'status',
            'image', 'min_age', 'has_certificate',
            'donation_kg_required', 'instructors',
            'next_lesson',
        ]

    def get_next_lesson(self, obj):
        # Reads from the prefetched `upcoming_lessons` attribute populated by
        # CourseViewSet.get_queryset. Falls back to a query for callers that
        # didn't go through the viewset.
        upcoming = getattr(obj, 'upcoming_lessons', None)
        if upcoming is None:
            from datetime import date
            upcoming = list(
                obj.lessons
                .filter(start_date__gte=date.today(), is_private=False)
                .order_by('start_date', 'start_time')[:1]
            )
        if not upcoming:
            return None
        return NextLessonSerializer(upcoming[0]).data


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = [
            'id', 'course', 'start_date', 'start_time', 'end_time',
            'capacity', 'instructor', 'label', 'is_private',
        ]
