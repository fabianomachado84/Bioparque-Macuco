"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView


admin.site.site_header = "Portal Macuco"
admin.site.site_title = "Portal Bioparque Macuco"
admin.site.index_title = "MacucoAdmin"

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('sobre/', TemplateView.as_view(template_name='about.html'), name='about'),
    path('cursos/', TemplateView.as_view(template_name='courses.html'), name='courses'),
    path(
        'cursos/<int:course_id>/',
        TemplateView.as_view(template_name='course_detail.html'),
        name='course_detail',
    ),
    path('inscricao/', TemplateView.as_view(template_name='enrollment.html'), name='enrollment'),
    path('admin/', admin.site.urls),
    path('api/', include('courses.urls')),
    path('api/', include('accounts.urls')),
    path('api/', include('enrollments.urls')),
    path('api/', include('content.urls')),
]

# In DEBUG, Django serves uploaded MEDIA files directly.
# In production, this is delegated to Nginx / a CDN / object storage.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
