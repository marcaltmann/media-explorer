from typing import Any
from django.contrib.auth.decorators import login_required
from django.db.models.query import QuerySet
from django.views import generic
from django.shortcuts import get_object_or_404, render
from rest_framework import permissions, viewsets

from archive.models import Resource, Collection, Person, Topic, Location
from archive.serializers import ResourceSerializer


class ResourceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows resources to be viewed or edited.
    """
    queryset = Resource.objects.all().order_by('anon_title')
    serializer_class = ResourceSerializer
    permission_classes = [permissions.IsAuthenticated]


def welcome(request):
    return render(request, "archive/welcome.html")


def search(request):
    q = request.GET.get("q", "")
    resources = Resource.objects.filter(title__contains=q).order_by("title")
    context = {
        "q": q,
        "resources": resources,
    }
    return render(request, "archive/search_results.html", context)


class CollectionIndexView(generic.ListView):
    template_name = "archive/collection_index.html"
    context_object_name = "collection_list"

    def get_queryset(self) -> QuerySet[Collection]:
        """Return collections ordered by name."""
        return Collection.objects.order_by("name")


class LocationIndexView(generic.ListView):
    template_name = "archive/location_index.html"
    context_object_name = "location_list"
    paginate_by = 25

    def get_queryset(self) -> QuerySet[Location]:
        """Return all locations."""
        return Location.objects.order_by("name")


class LocationDetailView(generic.DetailView):
    model = Location


def collection_detail(request, collection_id):
    collection = get_object_or_404(Collection, pk=collection_id)
    context = {
        "collection": collection,
        "resources": collection.resources.all(),
    }
    return render(request, "archive/collection_detail.html", context)


class ResourceIndexView(generic.ListView):
    template_name = "archive/resource_index.html"
    paginate_by = 12
    model = Resource


@login_required()
def resource_detail(request, resource_id):
    timecode = request.GET.get("tc", 0)
    resource = get_object_or_404(Resource, pk=resource_id)
    context = {
        "resource": resource,
        "timecode": timecode,
        "collections": resource.collection_set.all(),
        "transcripts": resource.transcript_set.all(),
    }
    return render(request, "archive/resource_detail.html", context)


def person_index(request):
    people = Person.objects.all
    context = {"people": people}
    return render(request, "archive/people/index.html", context)


def person_detail(request, person_id):
    person = get_object_or_404(Person, pk=person_id)
    context = {"person": person}
    return render(request, "archive/people/detail.html", context)


def topic_index(request):
    topics = Topic.objects.all
    context = {"topics": topics}
    return render(request, "archive/topics/index.html", context)


def topic_detail(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    context = {"topic": topic}
    return render(request, "archive/topics/detail.html", context)


@login_required()
def profile(request):
    context = {}
    return render(request, "archive/profile.html", context)