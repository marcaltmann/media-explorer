from django.shortcuts import render, get_object_or_404

from .models import Collection


def collection_index(request):
    collection_list = Collection.objects.all()

    context = {"collection_list": collection_list}

    return render(request, "media_collections/collection_index.html", context)


def collection_detail(request, pk: int):
    collection = get_object_or_404(Collection, pk=pk)
    resource_list = collection.resources.all()

    context = {"collection": collection, "resource_list": resource_list}

    return render(request, "media_collections/collection_detail.html", context)
