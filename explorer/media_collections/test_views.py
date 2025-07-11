import pytest
from pytest_django.asserts import assertContains

from explorer.resources.models import Resource
from .models import Collection
from .views import collection_index, collection_detail


@pytest.mark.django_db
def test_no_collections(rf):
    request = rf.get("/collections/")
    response = collection_index(request)

    assert response.status_code == 200
    assertContains(response, "<h1>Collections</h1>", html=True)
    assertContains(response, "There are no collections yet.", html=True)


@pytest.mark.django_db
def test_collection_index(rf):
    collection = Collection.objects.create(name="China")

    request = rf.get("/collections/")
    response = collection_index(request)

    assertContains(response, "<h1>Collections</h1>", html=True)
    assertContains(
        response, f"<a href='/collections/{collection.pk}/'>China</a>", html=True
    )


@pytest.mark.django_db
def test_collection_detail(rf):
    collection = Collection.objects.create(name="China")
    resource = Resource.objects.create(name="Forbidden City", collection=collection)

    request = rf.get(f"/collections/{collection.pk}/")
    response = collection_detail(request, collection.pk)

    assertContains(response, f"<h1>{collection.name}</h1>", html=True)
    assertContains(
        response,
        f"<a href='/collections/{collection.pk}/resources/{resource.pk}/'>Forbidden City</a>",
        html=True,
    )
