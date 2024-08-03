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
        for facet in self.facets:
            if isinstance(facet, FieldFacet):
                result += f"&facet.field={facet.solr_field}"
            elif isinstance(facet, RangeFacet):
                result += f"&facet.range={facet.solr_field}"
                result += f"&f.{facet.solr_field}.facet.range.start={facet.start}"
                result += f"&f.{facet.solr_field}.facet.range.end={facet.end}"
                result += f"&f.{facet.solr_field}.facet.range.gap={facet.gap}"
            else:
                raise ValueError("Unexpected facet type")
        return result


class Facet:
    def __init__(self, field: str, solr_field: str, verbose_name: str):
        self.field = field
        self.solr_field = solr_field
        self.verbose_name = verbose_name


class FieldFacet(Facet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class RangeFacet(Facet):
    def __init__(self, start=None, end=None, gap=None, **kwargs):
        self.start = start
        self.end = end
        self.gap = gap
        super().__init__(**kwargs)


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
