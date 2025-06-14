from django.shortcuts import render, get_object_or_404

from .models import Resource


def resource_detail(request, collection_pk: int, resource_pk: int):
    resource = get_object_or_404(Resource, pk=resource_pk, collection_id=collection_pk)
    media_file_list = resource.media_files.all()

    context = {"resource": resource, "media_file_list": media_file_list}

    return render(request, "resources/resource_detail.html", context)
