from rest_framework.routers import DefaultRouter
from .views import EmployeeViewSet, InstructorViewSet

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet, basename='employee')
router.register(r'instructors', InstructorViewSet, basename='instructor')

urlpatterns = router.urls