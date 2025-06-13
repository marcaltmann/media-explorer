from django.urls import path

from . import views

app_name = "media-collections"

urlpatterns = [
    path("", views.collection_index, name="collection-index"),
    path("<int:pk>", views.collection_detail, name="collection-detail")
]
