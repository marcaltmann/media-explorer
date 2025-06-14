from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path


urlpatterns = i18n_patterns(
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("collections/", include("explorer.media_collections.urls")),
    path("resources/", include("explorer.resources.urls")),
    path("", include("explorer.core.urls")),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DJANGO_ENV == "development":
    urlpatterns.append(path("__debug__/", include("debug_toolbar.urls")))
