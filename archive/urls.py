from django.urls import path

from . import views

app_name = "archive"

urlpatterns = [
    path("search/", views.search, name="search"),
    path("collections/", views.CollectionIndexView.as_view(), name="collection_index"),
    path(
        "collections/<int:collection_id>/",
        views.collection_detail,
        name="collection_detail",
    ),
    path("resources/", views.ResourceIndexView.as_view(), name="resource_index"),
    path("resources/<int:resource_id>/", views.resource_detail, name="resource_detail"),
    path(
        "resources/<int:resource_id>/bookmark/",
        views.bookmark_resource,
        name="bookmark_resource",
    ),
    path("agents/", views.agent_index, name="agent_index"),
    path("agents/<int:agent_id>/", views.agent_detail, name="agent_detail"),
]
