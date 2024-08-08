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
        q = QueryDict(mutable=True)
        q.setdefault("facet", "true")
        q.setdefault("facet.mincount", 1)
        for facet in self.facets:
            facet.solr_query_part(q)
            facet.solr_filter_part(q, self.params)

        print(q.urlencode())
        return q.urlencode()


class Facet:
    def __init__(
        self, field: str, solr_field: str, verbose_name: str, values: dict = None
    ) -> None:
        self.field = field
        self.solr_field = solr_field
        self.verbose_name = verbose_name
        self.values = values

    def solr_query_part(self, query: QueryDict) -> None:
        # Must be implemented by subclass.
        pass

    def solr_filter_part(self, query: QueryDict, params: QueryDict) -> None:
        # Must be implemented by subclass.
        pass


class FieldFacet(Facet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def solr_query_part(self, query: QueryDict) -> None:
        query.appendlist("facet.field", self.solr_field)

    def solr_filter_part(self, query: QueryDict, params: QueryDict) -> None:
        values = params.getlist(self.field)
        for value in values:
            query.appendlist("fq", f"{self.solr_field}:{value}")


class RangeFacet(Facet):
    def __init__(self, start=None, end=None, gap=None, **kwargs):
        self.start = start
        self.end = end
        self.gap = gap
        super().__init__(**kwargs)

    def solr_query_part(self, query: QueryDict) -> None:
        query.appendlist("facet.range", self.solr_field)
        query.setdefault(f"f.{self.solr_field}.facet.range.start", self.start)
        query.setdefault(f"f.{self.solr_field}.facet.range.end", self.end)
        query.setdefault(f"f.{self.solr_field}.facet.range.gap", self.gap)

    def solr_filter_part(self, query: QueryDict, params: QueryDict) -> None:
        pass


class ResourceFacetGroup(FacetGroup):
    facets = [
        FieldFacet(
            field="type",
            solr_field="type_s",
            verbose_name=(_("type")),
        ),
        FieldFacet(
            field="media_type",
            solr_field="media_type_s",
            verbose_name=(_("Media type")),
        ),
        FieldFacet(
            field="media_files_count",
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
            end="NOW+1YEAR/YEAR",
            gap="+1YEAR",
        ),
    ]
