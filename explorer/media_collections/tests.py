from django.test import TestCase
from django.urls import reverse

from .models import Collection


class CollectionTests(TestCase):
    def test_collection_index(self):
        collection = Collection.objects.create( name="China")

        response = self.client.get(reverse("media-collections:collection-index"))

        self.assertContains(response, "<h1>Collections</h1>", html=True)
        link_path = reverse(
            "media-collections:collection-detail", kwargs={"pk": collection.pk}
        )
        self.assertContains(response, f"<a href='{link_path}'>China</a>", html=True)

    def test_no_collections(self):
        response = self.client.get(reverse("media-collections:collection-index"))

        self.assertContains(response, "<h1>Collections</h1>", html=True)
        self.assertContains(response, "There are no collections yet.", html=True)
