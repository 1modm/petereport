"""petereport URL Configuration

"""

from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

from preport.views import markdown_uploader

urlpatterns = [
    # Needed for locale change
    path('i18n/', include('django.conf.urls.i18n')),
    path('martor/', include('martor.urls')),
    path('api/uploader/', markdown_uploader, name='markdown_uploader'),
]

urlpatterns += i18n_patterns(
    path('', include('preport.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.ADMIN_ENABLED:
    from django.contrib import admin
    urlpatterns += [
        path('admin/', admin.site.urls)
    ]
