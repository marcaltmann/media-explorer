from django.shortcuts import render, get_object_or_404

from .models import Collection


def collection_index(request):
    collections = Collection.objects.all()

    context = {"collections": collections}

    return render(request, "media_collections/collection_index.html", context)


def collection_detail(request, pk: int):
    collection = get_object_or_404(Collection, pk=pk)

    context = {"collection": collection}

    return render(request, "media_collections/collection_detail.html", context)
