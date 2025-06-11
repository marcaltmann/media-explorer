from django.contrib import admin

from .models import Archive


@admin.register(Archive)
class ArchiveAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]
