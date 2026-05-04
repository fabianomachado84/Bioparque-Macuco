from rest_framework.routers import SimpleRouter

from .views import BannerViewSet

router = SimpleRouter()
router.register(r'banners', BannerViewSet, basename='banner')

urlpatterns = router.urls
