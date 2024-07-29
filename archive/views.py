from requests import ConnectionError
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.views import generic
from django.views.decorators.http import require_GET, require_POST
from django.shortcuts import get_object_or_404, render, redirect

from archive.models import Resource, Collection, Agent, Agency, MediaFile
from search.query import query_resource
from accounts.models import Bookmark


class CollectionIndexView(generic.ListView):
    template_name = "archive/collection_index.html"
    context_object_name = "collection_list"

    def get_queryset(self) -> QuerySet[Collection]:
        """Return collections ordered by name."""
        return Collection.objects.order_by("name")


@require_GET
def collection_detail(request, collection_id):
    collection = get_object_or_404(Collection, pk=collection_id)
    context = {
        "collection": collection,
        "resources": collection.resources.all(),
    }
    return render(request, "archive/collection_detail.html", context)


@require_GET
def search(request):
    q = request.GET.get("q", "")

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


class ResourceIndexView(LoginRequiredMixin, generic.ListView):
    template_name = "archive/resource_index.html"
    paginate_by = 12
    model = Resource


@login_required
@require_GET
def resource_detail(request, resource_id):
    resource = get_object_or_404(Resource, pk=resource_id)
    first_media_file = resource.media_files.first()
    return redirect(first_media_file)


@login_required
@require_GET
def media_file_detail(request, resource_id, order):
    resource = get_object_or_404(Resource, pk=resource_id)
    media_files = resource.media_files.all()
    media_file = media_files[order]
    timecode = request.GET.get("tc", 0)
    user = request.user
    is_bookmarked = user.bookmark_set.filter(resource=resource).exists()
    context = {
        "resource": resource,
        "media_files": media_files,
        "media_file": media_file,
        "order": order,
        "timecode": timecode,
        "collections": resource.collection_set.all(),
        "transcripts": media_file.transcript_set.all(),
        "image_materials": resource.imagematerial_set.all(),
        "is_bookmarked": is_bookmarked,
    }
    return render(request, "archive/resource_detail.html", context)


@login_required
@require_POST
def bookmark_resource(request, resource_id):
    resource = get_object_or_404(Resource, pk=resource_id)
    user = request.user
    was_bookmarked = user.bookmark_set.filter(resource=resource).exists()
    if was_bookmarked:
        user.bookmark_set.filter(resource=resource).delete()
    else:
        Bookmark.objects.create(user=user, resource=resource)

    context = {"is_bookmarked": not was_bookmarked}
    return render(request, "archive/resource_bookmark_button.html", context=context)


@login_required
@require_GET
def agent_index(request):
    agents = Agent.objects.all()
    context = {"agents": agents}
    return render(request, "archive/agent_index.html", context=context)


@login_required
@require_GET
def agent_detail(request, agent_id):
    agent = get_object_or_404(Agent, pk=agent_id)
    agencies = agent.agency_set.all()
    context = {
        "agent": agent,
        "agencies": agencies,
    }
    return render(request, "archive/agent_detail.html", context=context)
