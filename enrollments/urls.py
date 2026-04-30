from rest_framework.routers import DefaultRouter
from .views import EnrollmentViewSet, PaymentViewSet, StudentViewSet

router = DefaultRouter()
router.register(r'enrollments', EnrollmentViewSet, basename='enrollment')
router.register(r'payments', PaymentViewSet, basename='payment')
router.register(r'students', StudentViewSet, basename='student')
urlpatterns = router.urls