from django.contrib import admin
from django.db.models import JSONField
from django_json_widget.widgets import JSONEditorWidget

from .models import Transcript, TextMaterial, ImageMaterial


@admin.register(Transcript)
class TranscriptAdmin(admin.ModelAdmin):
    search_fields = ["vtt"]
    list_display = ["media_file", "language"]
    formfield_overrides = {
        JSONField: {"widget": JSONEditorWidget},
    }


@admin.register(TextMaterial)
class TextMaterialAdmin(admin.ModelAdmin):
    search_fields = ["identifier", "caption", "content"]
    list_display = ["resource", "identifier", "caption", "date"]


@admin.register(ImageMaterial)
class ImageMaterialAdmin(admin.ModelAdmin):
    search_fields = ["identifier", "caption"]
    list_display = ["resource", "identifier", "caption", "date"]
