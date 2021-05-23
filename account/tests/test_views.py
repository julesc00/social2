from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

CREATE_USER_URL = reverse("account:register")
# TOKEN_URL = reverse("user:token")
# ME_URL = reverse("user:me")


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserTests(TestCase):
    """Test the public endpoints."""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_successful(self):
        """Test creating a user with valid payload is successful."""
        payload = {
            "username": "testuser",
            "first_name": "Testuser",
            "email": "test@nowhere.com",
            "password": "testpass",
            "password2": "testpass",

        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload["password"]))

    def test_user_exists(self):
        """Test creating an existing user fails."""
        payload = {
            "username": "testuser",
            "password": "testpass",
            "first_name": "Testuser"
        }

        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


class PrivateUserApiTests(TestCase):
    """Test API requests that require authentication."""

    def setUp(self):
        self.user = create_user(
            username="testuser",
            password="testpass",

        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_user_login(self):
        """Test user log in successful."""
        res = self.client.get("account:login")

        self.assertEqual(res.status_code, status.HTTP_200_OK)

