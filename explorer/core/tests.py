from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse


class FooterTests(TestCase):
    def test_external_links(self):
        """Test external links"""
        response = self.client.get(reverse("core:welcome"))

        self.assertContains(response, "https://github.com/marcaltmann/explorer")


class CorePagesTests(TestCase):
    def test_welcome_page(self):
        response = self.client.get(reverse("core:welcome"))

        self.assertContains(
            response, "<h1 class='hero__title'>Explorer</h1>", html=True
        )

    def test_privacy_page(self):
        response = self.client.get(reverse("core:privacy"))

        self.assertContains(response, "<h1>Privacy</h1>", html=True)

    def test_contact_page(self):
        response = self.client.get(reverse("core:contact"))

        self.assertContains(response, "<h1>Contact</h1>", html=True)

    def test_accessibility_page(self):
        response = self.client.get(reverse("core:accessibility"))

        self.assertContains(response, "<h1>Accessibility</h1>", html=True)

    def test_terms_page(self):
        response = self.client.get(reverse("core:terms"))

        self.assertContains(response, "<h1>Terms of Use</h1>", html=True)

    def test_legal_notice_page(self):
        response = self.client.get(reverse("core:legal_notice"))

        self.assertContains(response, "<h1>Legal Notice</h1>", html=True)
