from rest_framework.routers import DefaultRouter
from .views import EnrollmentViewSet, PaymentViewSet

router = DefaultRouter()
router.register(r'enrollments', EnrollmentViewSet, basename='enrollment')
router.register(r'payments', PaymentViewSet, basename='payment')
urlpatterns = router.urls