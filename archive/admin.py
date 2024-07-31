from django.contrib import admin

from archive.models import (
    MediaFile,
    Resource,
    Collection,
    Agent,
    Agency,
    MetadataKey,
    CharFieldMetadata,
    EntityReference,
)


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    search_fields = ["last_name", "first_name"]
    list_display = ["last_name", "first_name", "gender", "date_of_birth"]


class EntityReferenceInline(admin.TabularInline):
    model = EntityReference
    extra = 0


class AgencyInline(admin.TabularInline):
    model = Agency
    extra = 0


class MediaFileInline(admin.TabularInline):
    model = MediaFile
    extra = 0


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    list_display = ["title", "type", "public"]
    list_filter = ["public"]
    fieldsets = [
        (None, {"fields": ["title", "description", "public"]}),
        (
            "Media information",
            {"fields": ["type"]},
        ),
    ]
    inlines = [
        MediaFileInline,
        AgencyInline,
        EntityReferenceInline,
    ]


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    search_fields = ["name", "description"]
    fields = ["name", "description", "resources"]
    list_display = ["name", "resource_count"]
    filter_horizontal = ["resources"]


@admin.register(MetadataKey)
class MetadataKeyAdmin(admin.ModelAdmin):
    search_fields = ["label"]
    list_display = ["label"]


@admin.register(CharFieldMetadata)
class CharFieldMetadataAdmin(admin.ModelAdmin):
    list_display = ["resource", "key", "value"]
