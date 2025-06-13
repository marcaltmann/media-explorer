from django.urls import path

from . import views

app_name = "resources"

urlpatterns = [path("<int:pk>", views.resource_detail, name="resource-detail")]
