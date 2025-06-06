from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse


class CorePagesTests(TestCase):
    def test_welcome_page(self):
        response = self.client.get(reverse("core:welcome"), follow=True)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(
            response, "<h1 class='hero__title'>Explorer</h1>", html=True
        )

    def test_privacy_page(self):
        response = self.client.get(reverse("core:privacy"), follow=True)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "<h1>Privacy</h1>", html=True)

    def test_contact_page(self):
        response = self.client.get(reverse("core:contact"), follow=True)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "<h1>Contact</h1>", html=True)

    def test_accessibility_page(self):
        response = self.client.get(reverse("core:accessibility"), follow=True)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "<h1>Accessibility</h1>", html=True)

    def test_terms_page(self):
        response = self.client.get(reverse("core:terms"), follow=True)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "<h1>Terms of Use</h1>", html=True)

    def test_legal_notice_page(self):
        response = self.client.get(reverse("core:legal_notice"), follow=True)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "<h1>Legal Notice</h1>", html=True)
