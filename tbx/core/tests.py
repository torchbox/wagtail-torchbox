from django.test import TestCase
from django.urls import reverse


class SecurityViewTestCase(TestCase):
    url = reverse("security-txt")

    def test_accessible(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["security_txt"],
            "http://testserver/.well-known/security.txt",
        )
        self.assertIn("no-cache", response["Cache-Control"])
