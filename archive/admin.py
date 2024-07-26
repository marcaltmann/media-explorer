from django.contrib import admin

from archive.models import (
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
    extra = 1


class AgencyInline(admin.TabularInline):
    model = Agency
    extra = 1


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    list_display = ["title", "type", "media_type", "duration", "public", "is_video"]
    list_filter = ["production_date", "media_type", "public"]
    fieldsets = [
        (None, {"fields": ["title", "production_date", "duration", "public"]}),
        (
            "Media information",
            {"fields": ["type", "media_type", "media_url", "poster"]},
        ),
    ]
    inlines = [
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
