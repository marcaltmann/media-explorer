from django.urls import path

from . import views

app_name = "resources"

urlpatterns = [
    path(
        "<int:collection_pk>/resources/<int:resource_pk>/",
        views.resource_detail,
        name="resource-detail",
    ),
]
