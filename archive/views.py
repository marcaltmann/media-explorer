from requests import ConnectionError
from django.contrib.auth.decorators import login_required
from django.db.models.query import QuerySet
from django.views import generic
from django.shortcuts import get_object_or_404, render, redirect

from archive.models import Resource, Collection
from search.query import query_resource
from accounts.models import Bookmark


class CollectionIndexView(generic.ListView):
    template_name = "archive/collection_index.html"
    context_object_name = "collection_list"

    def get_queryset(self) -> QuerySet[Collection]:
        """Return collections ordered by name."""
        return Collection.objects.order_by("name")


def collection_detail(request, collection_id):
    collection = get_object_or_404(Collection, pk=collection_id)
    context = {
        "collection": collection,
        "resources": collection.resources.all(),
    }
    return render(request, "archive/collection_detail.html", context)


def search(request):
    q = request.GET.get("q", "") or "*"

    try:
        resources, count = query_resource(q)  # These are Solr docs.
        context = {
            "q": q,
            "resources": resources,
            "count": count,
        }
        return render(request, "archive/search_results.html", context)
    except ConnectionError as e:
        context = {
            "q": q,
        }
        return render(request, "archive/search_error.html", context)


class ResourceIndexView(generic.ListView):
    template_name = "archive/resource_index.html"
    paginate_by = 12
    model = Resource


@login_required()
def resource_detail(request, resource_id):
    resource = get_object_or_404(Resource, pk=resource_id)
    timecode = request.GET.get("tc", 0)
    user = request.user
    is_bookmarked = user.bookmark_set.filter(resource=resource).exists()
    context = {
        "resource": resource,
        "timecode": timecode,
        "collections": resource.collection_set.all(),
        "transcripts": resource.transcript_set.all(),
        "image_materials": resource.imagematerial_set.all(),
        "is_bookmarked": is_bookmarked,
    }
    return render(request, "archive/resource_detail.html", context)


@login_required()
def bookmark_resource(request, resource_id):
    resource = get_object_or_404(Resource, pk=resource_id)
    user = request.user
    is_bookmarked = user.bookmark_set.filter(resource=resource).exists()
    if is_bookmarked:
        user.bookmark_set.filter(resource=resource).delete()
    else:
        Bookmark.objects.create(user=user, resource=resource)
    return redirect("archive:resource_detail", resource_id=resource_id)
