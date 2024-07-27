from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_GET

from .models import ImageMaterial, Transcript


@login_required
@require_GET
def image_material_detail(request, image_material_id):
    image_material = get_object_or_404(ImageMaterial, pk=image_material_id)
    resource = image_material.resource
    context = {
        "image_material": image_material,
        "resource": resource,
    }
    return render(request, "materials/image_material_detail.html", context)


@login_required
@require_GET
def transcript_vtt(request, transcript_id):
    transcript = get_object_or_404(Transcript, pk=transcript_id)
    return HttpResponse(transcript.vtt, content_type="text/vtt")
