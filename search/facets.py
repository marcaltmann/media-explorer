class BaseFacetGroup:
    def __init__(self, facets):
        self.facets = facets


class BaseFacet:
    pass


class FieldFacet(BaseFacet):
    def __init__(self, field=None):
        self.field = field


class RangeFacet(BaseFacet):
    def __init__(self, field=None, start=None, end=None, gap=None):
        self.field = field


class ResourceFacetGroup(BaseFacetGroup):
    media_type = FieldFacet(field="media_type_s")
    media_files_count = FieldFacet(field="media_files_count_i")
    duration = RangeFacet(field="duration_i", start="0", end="36000", gap="1800")
    production_date = RangeFacet(
        field="production_date_dt", start="0", end="0", gap="0"
    )
