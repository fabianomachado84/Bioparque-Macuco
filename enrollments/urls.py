from rest_framework.routers import SimpleRouter
from django.urls import path

from .views import (
    EnrollmentViewSet,
    PaymentViewSet,
    StudentViewSet,
    revenue_by_course_and_month,
    donations_by_type,
    students_age_groups,
    admin_reports,  
)

router = SimpleRouter()

router.register(r'enrollments', EnrollmentViewSet, basename='enrollment')
router.register(r'payments', PaymentViewSet, basename='payment')
router.register(r'students', StudentViewSet, basename='student')

urlpatterns = router.urls

urlpatterns += [
    path(
        'reports/revenue/',
        revenue_by_course_and_month
    ),

    path(
        'reports/donations/',
        donations_by_type
    ),

    path(
        'reports/age-groups/',
        students_age_groups
    ),
    path(
        'admin/reports/',
        admin_reports
    ),
]