from rest_framework.routers import SimpleRouter
from .views import EmployeeViewSet, InstructorViewSet

router = SimpleRouter()
router.register(r'employees', EmployeeViewSet, basename='employee')
router.register(r'instructors', InstructorViewSet, basename='instructor')

urlpatterns = router.urls