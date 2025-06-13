from django.shortcuts import render, get_object_or_404

from .models import Resource


def resource_detail(request, pk: int):
    resource = get_object_or_404(Resource, pk=pk)
    media_file_list = resource.media_files.all()

    context = {"resource": resource, "media_file_list": media_file_list}

    return render(request, "resources/resource_detail.html", context)
