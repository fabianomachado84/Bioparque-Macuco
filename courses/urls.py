from rest_framework.routers import SimpleRouter
from .views import CourseViewSet, LessonViewSet

router = SimpleRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'lessons', LessonViewSet, basename='lesson')
urlpatterns = router.urls