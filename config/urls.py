from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('apps.accounts.urls')),
    path('subjects/', include('apps.subjects.urls')),
    path('resources/', include('apps.resources.urls')),
    path('api/subjects/', include('apps.subjects.api_urls')),
    path('api/resources/', include('apps.resources.api_urls')),
    path('', RedirectView.as_view(url='/subjects/', permanent=False)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
