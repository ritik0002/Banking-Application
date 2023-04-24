from django.test import TestCase

# Create your tests here.
from django.contrib.auth.models import User

class Login(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username="testuser", password="testpass")

    def test_login_success(self):
        # Test if login is successful with correct credentials
        response = self.client.post("/login/", {"username": "testuser", "password": "testpass"})
        # Check if user is logged in
        self.assertTrue(response.context["user"].is_authenticated)
        # Check if response is a redirect to the expected url
        self.assertRedirects(response, "/users/secure/")

    def test_login_failure(self):
        # Test if login fails with wrong credentials
        response = self.client.post("/login/", {"username": "testuser", "password": "wrongpass"})
        # Check if user is not logged in
        self.assertFalse(response.context["user"].is_authenticated)
        # Check if response is not a redirect but has a status code 200 (OK)
        self.assertEqual(response.status_code, 200)
        # Check if the form has an error message
        self.assertFormError(response, "form", None, "Please enter a correct username and password. Note that both fields may be case-sensitive.")