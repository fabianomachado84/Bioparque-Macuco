from datetime import date

from django.db.models import F, Min, Prefetch, Q
from rest_framework import mixins, viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer


class CourseViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """Public, read-only catalog of courses.

    Anyone can list and retrieve; writes are not exposed through the API and
    must go through the Django Admin.

    Default behavior:
    - Only `status='active'` courses are returned (override with `?status=`).
    - Ordered by the date of the next upcoming public lesson, with courses
      that have no future lessons sorted last.
    - Allows `?ordering=name` / `?ordering=-name` / `?ordering=price`,
      etc., when the front needs a different sort.
    """

    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [OrderingFilter]
    ordering_fields = ['name', 'price', 'duration_hours', 'created_at']

    def get_queryset(self):
        today = date.today()

        upcoming_lessons_qs = Lesson.objects.filter(
            start_date__gte=today,
            is_private=False,
        ).order_by('start_date', 'start_time')

        qs = (
            Course.objects
            .prefetch_related(
                Prefetch('lessons', queryset=upcoming_lessons_qs, to_attr='upcoming_lessons'),
                'instructors__employee__user',
            )
            .annotate(
                next_lesson_date=Min(
                    'lessons__start_date',
                    filter=Q(lessons__start_date__gte=today, lessons__is_private=False),
                ),
            )
        )

        # Default to active courses; allow explicit override (e.g. ?status=inactive).
        status_param = self.request.query_params.get('status', 'active')
        if status_param:
            qs = qs.filter(status=status_param)

        # When the client did not request an explicit ordering, sort by
        # the schedule (closest upcoming lesson first, NULLs last).
        if not self.request.query_params.get('ordering'):
            qs = qs.order_by(F('next_lesson_date').asc(nulls_last=True), 'name')

        return qs


class LessonViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """Public, read-only catalog of lessons (turmas).

    Hides `is_private=True` lessons from anonymous callers (only authenticated
    users can see closed groups via the API; writes go through the Django
    Admin). Supports `?course=<id>` to fetch the lessons of a single course.
    """

    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [OrderingFilter]
    ordering_fields = ['start_date', 'start_time']
    ordering = ['start_date', 'start_time']

    def get_queryset(self):
        qs = Lesson.objects.select_related('course', 'instructor__employee__user')

        # Anonymous users never see private lessons.
        if not self.request.user.is_authenticated:
            qs = qs.filter(is_private=False)

        course_id = self.request.query_params.get('course')
        if course_id:
            qs = qs.filter(course_id=course_id)

        return qs
