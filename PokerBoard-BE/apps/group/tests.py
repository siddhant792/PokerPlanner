from django.contrib.auth import get_user_model
from django.urls import reverse

from ddf import G
from rest_framework.test import APITestCase

from apps.group import (
    constants as pokerboard_constants,
    models as group_models,
)
from apps.user import models as user_models


class GroupTestCases(APITestCase):
    """
    Group testcases for testing group list, details and add member functionality
    """
    GROUP_URL = reverse('groups-list')
    CREATE_MEMBER_URL = reverse('create-members')

    def setUp(self):
        """
        Setup method for creating default user and it's token
        """

        self.user = G(get_user_model())
        token = G(user_models.Token, user=self.user)
        self.group = G(group_models.Group, created_by=self.user, name="Kung fu panda")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_create_group(self):
        """
        Creates group, check for it's name and default group member
        """
        data = {
            "name": "Dominos"
        }
        response = self.client.post(self.GROUP_URL, data=data)
        expected_member = group_models.GroupMember.objects.get(group__name="Dominos")
        group = expected_member.group
        expected_data = {
            "id": group.id,
            "name": group.name,
            "created_by": self.user.id,
            "created_at": group.created_at.strftime(pokerboard_constants.DATETIME_FORMAT),
            "updated_at": group.updated_at.strftime(pokerboard_constants.DATETIME_FORMAT),
            "members": [
                {
                    "id": expected_member.id,
                    "group": expected_member.group.id,
                    "user": {
                        "id": expected_member.user.id,
                        "email": expected_member.user.email,
                        "first_name": expected_member.user.first_name,
                        "last_name": expected_member.user.last_name,
                    },
                    "created_at": expected_member.created_at.strftime(pokerboard_constants.DATETIME_FORMAT),
                    "updated_at": expected_member.updated_at.strftime(pokerboard_constants.DATETIME_FORMAT),
                }
            ]
        }
        self.assertEqual(response.status_code, 201)
        self.assertDictEqual(expected_data, response.data)

    def test_create_group_unique_name(self):
        """
        Creates group, expects 400 response code on non-unique name
        """
        data = {
            "name": self.group.name,
        }
        expected_data = {
            "name": [
                "group with this name already exists."
            ]
        }
        response = self.client.post(self.GROUP_URL, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.data, expected_data)

    def test_create_group_failure_empty_name(self):
        """
        Create group, expects bad request on empty group name
        """
        data = {
            "name": ""
        }
        expected_data = {
            "name": [
                "This field may not be blank."
            ]
        }
        response = self.client.post(self.GROUP_URL, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.data, expected_data)

    def test_create_group_failure_without_name(self):
        """
        Create group, expects bad request on no group name
        """
        data = {}
        expected_data = {
            "name": [
                "This field is required."
            ]
        }
        response = self.client.post(self.GROUP_URL, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.data, expected_data)

    def test_list_group(self):
        """
        Get group list, checks for only group's name
        """
        response = self.client.get(self.GROUP_URL)
        expected_member = group_models.GroupMember.objects.get(group=self.group)

        expected_data = [
            {
                "id": self.group.id,
                "name": self.group.name,
                "created_by": self.user.id,
                "created_at": self.group.created_at.strftime(pokerboard_constants.DATETIME_FORMAT),
                "updated_at": self.group.updated_at.strftime(pokerboard_constants.DATETIME_FORMAT),
                "members": [
                    {
                        "id": expected_member.id,
                        "group": expected_member.group.id,
                        "user": {
                            "id": expected_member.user.id,
                            "email": expected_member.user.email,
                            "first_name": expected_member.user.first_name,
                            "last_name": expected_member.user.last_name,
                        },
                        "created_at": expected_member.created_at.strftime(pokerboard_constants.DATETIME_FORMAT),
                        "updated_at": expected_member.updated_at.strftime(pokerboard_constants.DATETIME_FORMAT),
                    }
                ]
            }
        ]
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(expected_data, response.data)

    def test_get_group_details(self):
        """
        Get group details by groupId, Expects 200 response code
        """
        expected_member = group_models.GroupMember.objects.get(group=self.group)
        expected_data = {
            "id": self.group.id,
            "name": self.group.name,
            "created_by": self.user.id,
            "created_at": self.group.created_at.strftime(pokerboard_constants.DATETIME_FORMAT),
            "updated_at": self.group.updated_at.strftime(pokerboard_constants.DATETIME_FORMAT),
            "members": [
                {
                    "id": expected_member.id,
                    "group": expected_member.group.id,
                    "user": {
                        "id": expected_member.user.id,
                        "email": expected_member.user.email,
                        "first_name": expected_member.user.first_name,
                        "last_name": expected_member.user.last_name,
                    },
                    "created_at": expected_member.created_at.strftime(pokerboard_constants.DATETIME_FORMAT),
                    "updated_at": expected_member.updated_at.strftime(pokerboard_constants.DATETIME_FORMAT),
                }
            ]
        }
        response = self.client.get(reverse('groups-detail', args=[self.group.id]))
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(expected_data, response.data)

    def test_get_group_details_not_found(self):
        """
        Get group details by groupId, Expects 404 on invalid groupId
        """
        response = self.client.get(reverse('groups-detail', args=[7]))
        self.assertEqual(response.status_code, 404)

    def test_add_member_to_group(self):
        """
        Add member to group, Expects 201 response code
        """
        user = G(get_user_model())
        data = {
            "group": self.group.id,
            "email": user.email
        }
        response = self.client.post(self.CREATE_MEMBER_URL, data=data)
        expected_member = group_models.GroupMember.objects.get(group=self.group, user=user)   
        expected_data = {
            "group": expected_member.group.id,
            "user": {
                "id": expected_member.user.id,
                "email": expected_member.user.email,
                "first_name": expected_member.user.first_name,
                "last_name": expected_member.user.last_name,
            }
        }
        self.assertEqual(response.status_code, 201)
        self.assertDictEqual(response.data, expected_data)

    def test_add_member_failure_without_email(self):
        """
        Add member to group, Expects 400 response code on not providing email
        """
        data = {
            "group": self.group.id
        }
        expected_data = {
            "email": [
                "This field is required."
            ]
        }
        response = self.client.post(self.CREATE_MEMBER_URL, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.data, expected_data)
    
    def test_add_member_failure_without_group(self):
        """
        Add member to group, Expects 400 response code on not providing group
        """
        user_2 = G(get_user_model())
        data = {
            "email": user_2.email
        }
        expected_data = {
            "group": [
                "This field is required."
            ]
        }

        response = self.client.post(self.CREATE_MEMBER_URL, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.data, expected_data)
    
    def test_add_member_multiple_times(self):
        """
        Add member to group, Expects 400 response code on adding a member two times
        """
        data = {
            "group": self.group.id,
            "email": self.user.email
        }
        expected_data = {
            "non_field_errors": [
                "A member can't be added to a group twice"
            ]
        }
        response = self.client.post(self.CREATE_MEMBER_URL, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.data, expected_data)

    def test_add_member_for_non_existing_member(self):
        """
        Add member to group, Expects 400 response code on providing unregistered email
        """
        data = {
            "group": self.group.id,
            "email": "dummy@dummy.com"
        }
        expected_data = {
            "non_field_errors": [
                "No such user"
            ]
        }
        response = self.client.post(self.CREATE_MEMBER_URL, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.data, expected_data)
