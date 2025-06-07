from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path
from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = (
    i18n_patterns(
        path("admin/", admin.site.urls),
        path("accounts/", include("allauth.urls")),
        path("", include("explorer.core.urls")),
    )
    + debug_toolbar_urls()
)
