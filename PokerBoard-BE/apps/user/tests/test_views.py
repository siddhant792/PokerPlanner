from ddf import G

from rest_framework.test import APITestCase

from django.contrib.auth import get_user_model
from django.urls import reverse

from apps.user import models as user_models


class PokerboardTestCases(APITestCase):
    REGISTER_URL = reverse('register')
    LOGIN_URL = reverse('login')

    def setUp(self: APITestCase) -> None:
        """
        Setup method for creating default user and it's token
        """
        self.user = G(get_user_model())
        token = G(user_models.Token, user=self.user).key
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

    def test_create_user(self: APITestCase) -> None:
        """
        Test create user
        """
        data = {
            "first_name": "Siddhant",
            "last_name": "Gupta",
            "email": "siddhant.gupta@joshtechnologygroup.com",
            "password": "Password@123",
        }
        response = self.client.post(self.REGISTER_URL, data=data)
        self.assertEqual(response.status_code, 201)
        user = user_models.User.objects.filter(email=data["email"]).first()
        self.assertIsNotNone(user)
        expected_data = {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
        }
        self.assertDictEqual(expected_data, response.data)

    def test_create_user_without_first_name(self: APITestCase) -> None:
        """
        Test create user without first_name
        """
        data = {
            "last_name": "Gupta",
            "email": "siddhant.gupta@joshtechnologygroup.com",
            "password": "Password@123",
        }
        expected_data = {
            "first_name": [
                "This field is required."
            ]
        }
        response = self.client.post(self.REGISTER_URL, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(expected_data, response.data)

    def test_create_user_without_last_name(self: APITestCase) -> None:
        """
        Test create user without last_name
        """
        data = {
            "first_name": "Siddhant",
            "email": "siddhant.gupta@joshtechnologygroup.com",
            "password": "Password@123",
        }
        expected_data = {
            "last_name": [
                "This field is required."
            ]
        }
        response = self.client.post(self.REGISTER_URL, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(expected_data, response.data)

    def test_create_user_without_email(self: APITestCase) -> None:
        """
        Test create user without email
        """
        data = {
            "first_name": "Siddhant",
            "last_name": "Gupta",
            "password": "Password@123",
        }
        expected_data = {
            "email": [
                "This field is required."
            ]
        }
        response = self.client.post(self.REGISTER_URL, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(expected_data, response.data)

    def test_create_user_with_invalid_email(self: APITestCase) -> None:
        """
        Test create user with invalid email
        """
        data = {
            "first_name": "Siddhant",
            "last_name": "Gupta",
            "email": "siddhant123gmail.com",
            "password": "Password@123",
        }
        expected_data = {
            "email": [
                "Enter a valid email address."
            ]
        }
        response = self.client.post(self.REGISTER_URL, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(expected_data, response.data)

    def test_create_user_without_password(self: APITestCase) -> None:
        """
        Test create user without password
        """
        data = {
            "first_name": "Siddhant",
            "last_name": "Gupta",
            "email": "siddhant.gupta@joshtechnologygroup.com",
        }
        expected_data = {
            "password": [
                "This field is required."
            ]
        }
        response = self.client.post(self.REGISTER_URL, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(expected_data, response.data)

    def test_update_user_first_name(self: APITestCase) -> None:
        """
        Test update user first name
        """
        data = {
            "first_name": "Akash",
        }
        expected_data = {
            "id": self.user.id,
            "first_name": data['first_name'],
            "last_name": self.user.last_name,
            "email": self.user.email,
        }
        url = reverse('user', args=[self.user.id])
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(expected_data, response.data)

    def test_update_user_last_name(self: APITestCase) -> None:
        """
        Test update user last name
        """
        data = {
            "last_name": "Singh",
        }
        expected_data = {
            "id": self.user.id,
            "first_name": self.user.first_name,
            "last_name": data['last_name'],
            "email": self.user.email,
        }
        url = reverse('user', args=[self.user.id])
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(expected_data, response.data)

    def test_update_user_password(self: APITestCase) -> None:
        """
        Test update user password
        """
        data = {
            "password": "Tar1232@suef",
        }
        expected_data = {
            "id": self.user.id,
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
            "email": self.user.email,
        }
        url = reverse('user', args=[self.user.id])
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(expected_data, response.data)
