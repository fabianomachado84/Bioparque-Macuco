from rest_framework import serializers

from .models import Banner


class BannerSerializer(serializers.ModelSerializer):
    """Public banner representation. Internal fields like `name` are kept off the wire."""

    class Meta:
        model = Banner
        fields = [
            'id', 'image', 'title', 'subtitle',
            'link_url', 'link_label', 'display_order',
        ]
