from django.http import QueryDict
from django.utils.translation import gettext_lazy as _


class FacetGroup:
    """
    Initialized with the query params sent by the browser.
    """

    facets = []

    def __init__(self, params: QueryDict = None) -> None:
        self.params = params or QueryDict()

    def solr_query(self) -> str:
        result = "facet=true&facet.mincount=1"
        result += "".join([facet.solr_query_part() for facet in self.facets])
        return result


class Facet:
    def __init__(self, field: str, solr_field: str, verbose_name: str):
        self.field = field
        self.solr_field = solr_field
        self.verbose_name = verbose_name

    def solr_query_part(self) -> str:
        # Must be implemented by subclass.
        pass


class FieldFacet(Facet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def solr_query_part(self) -> str:
        return f"&facet.field={self.solr_field}"


class RangeFacet(Facet):
    def __init__(self, start=None, end=None, gap=None, **kwargs):
        self.start = start
        self.end = end
        self.gap = gap
        super().__init__(**kwargs)

    def solr_query_part(self) -> str:
        result = f"&facet.range={self.solr_field}"
        result += f"&f.{self.solr_field}.facet.range.start={self.start}"
        result += f"&f.{self.solr_field}.facet.range.end={self.end}"
        result += f"&f.{self.solr_field}.facet.range.gap={self.gap}"
        return result


class ResourceFacetGroup(FacetGroup):
    facets = [
        FieldFacet(
            field="media_type",
            solr_field="media_type_s",
            verbose_name=(_("Media type")),
        ),
        FieldFacet(
            field="media_files_count_i",
            solr_field="media_files_count_i",
            verbose_name=_("Media files count"),
        ),
        RangeFacet(
            field="duration",
            solr_field="duration_i",
            verbose_name=_("Duration"),
            start="0",
            end="36000",
            gap="1800",
        ),
        RangeFacet(
            field="production_date",
            solr_field="production_date_dt",
            verbose_name=_("Production date"),
            start="1900-01-01T00:00:00Z/YEAR",
            end="NOW%2B1YEAR/YEAR",
            gap="%2B1YEAR",
        ),
    ]
