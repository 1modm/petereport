"""petereport URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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

from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

from preport.views import markdown_uploader

urlpatterns = [
    # Needed for locale change
    path('i18n/', include('django.conf.urls.i18n')),
    path('martor/api/uploader/', markdown_uploader, name='markdown_uploader_page'),
    path('martor/', include('martor.urls')),
]
urlpatterns += i18n_patterns(
    path('', include('preport.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.ADMIN_ENABLED:
    from django.contrib import admin
    urlpatterns += [
        path('grappelli/', include('grappelli.urls')),
        path('admin/', admin.site.urls)
    ]