from django.test import TestCase
from django.urls import reverse

from .models import Collection


class CorePagesTests(TestCase):
    def test_welcome_page(self):
        collection = Collection.objects.create(name="China")

        response = self.client.get(reverse("media-collections:collection-index"))

        self.assertContains(response, "<h1>Collections</h1>", html=True)
        link_path = reverse(
            "media-collections:collection-detail", kwargs={"pk": collection.pk}
        )
        self.assertContains(response, f"<a href='{link_path}'>China</a>", html=True)
