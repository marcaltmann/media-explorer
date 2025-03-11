from http import HTTPStatus

from django.test import TestCase


class AddBookFormTests(TestCase):
    def test_welcome_page(self):
        response = self.client.get("/", follow=True)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(
            response, "<h1 class='h1 hero__title'>Explorer</h1>", html=True
        )
