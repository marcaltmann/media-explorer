from django.test import TestCase
from django.urls import reverse

from .models import Collection
from explorer.resources.models import Resource


class CollectionTests(TestCase):
    def test_collection_index(self):
        """The collection index page presents links to all collections."""
        collection = Collection.objects.create(name="China")

        response = self.client.get(reverse("media-collections:collection-index"))

        self.assertContains(response, "<h1>Collections</h1>", html=True)
        link_path = reverse(
            "media-collections:collection-detail", kwargs={"pk": collection.pk}
        )
        self.assertContains(response, f"<a href='{link_path}'>China</a>", html=True)

    def test_no_collections(self):
        """If no collections are available, a message is displayed."""
        response = self.client.get(reverse("media-collections:collection-index"))

        self.assertContains(response, "<h1>Collections</h1>", html=True)
        self.assertContains(response, "There are no collections yet.", html=True)

    def test_collection_detail(self):
        """The collection detail page presents links to its resources."""
        collection = Collection.objects.create(name="China")
        resource = Resource.objects.create(name="Forbidden City", collection=collection)

        response = self.client.get(
            reverse("media-collections:collection-detail", args=[collection.pk])
        )

        self.assertContains(response, f"<h1>{collection.name}</h1>", html=True)
        link_path = reverse(
            "resources:resource-detail", args=[collection.pk, resource.pk]
        )
        self.assertContains(
            response, f"<a href='{link_path}'>Forbidden City</a>", html=True
        )
