from django.contrib import admin

from .models import Resource, MediaFile


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ["name"]

@admin.register(MediaFile)
class MediaFileAdmin(admin.ModelAdmin):
    list_display = ["name", "order"]
