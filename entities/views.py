from django.shortcuts import get_object_or_404, render

from .models import Entity


def entity_index(request):
    type_filter = request.GET.get("type")
    if type_filter:
        entities = Entity.objects.filter(type=type_filter)
    else:
        entities = Entity.objects.all()

    context = {
        "entities": entities,
        "type_filter": type_filter,
        "type_choices": Entity.TYPE_CHOICES,
    }
    return render(request, "entities/entity_index.html", context)


def entity_detail(request, entity_id):
    entity = get_object_or_404(Entity, pk=entity_id)
    context = {"entity": entity}
    return render(request, "entities/entity_detail.html", context)
