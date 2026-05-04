from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Banner
from .serializers import BannerSerializer


class BannerViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """Public, read-only feed of banners currently scheduled for display.

    Hides inactive banners and respects start/end dates so the front never
    receives banners outside their validity window. Writes go through the
    Django Admin only.
    """

    serializer_class = BannerSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = None

    def get_queryset(self):
        return Banner.objects.visible_today()
