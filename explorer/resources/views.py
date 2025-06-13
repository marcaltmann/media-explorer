from django.shortcuts import render, get_object_or_404

from .models import Resource


def resource_detail(request, pk: int):
    resource = get_object_or_404(Resource, pk=pk)

    context = { "resource": resource }

    return render(request, "resources/resource_detail.html", context)
