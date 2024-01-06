from rest_framework.test import APITestCase
from django.urls import reverse

from modules.serializers import ModuleSerializer
from users.models import User
from rest_framework import status

from django.test import TestCase

from modules.models import Module


class ModuleTest(TestCase):
    """Тест для модели модуля."""

    def setUp(self):
        Module.objects.create(
            number=1,
            name='Test',
            description='Test description'
        )

    def test_module_name(self):
        module = Module.objects.get(number=1)
        self.assertEqual(module.name, 'Test')


class ModuleSerializerTest(TestCase):
    """Тест для ModuleSerializer"""
    def setUp(self):
        self.module = Module.objects.create(
            number=1,
            name='Test',
            description='Test description'
        )
        self.serializer = ModuleSerializer(instance=self.module)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'number', 'name', 'description', 'owner']))


class ModuleTestCase(APITestCase):
    """Тест для Model Views"""
    def setUp(self):
        self.user = User.objects.create(email='test@test.com', is_staff=True, is_superuser=True)
        self.user.set_password('1234')
        self.user.save()

        response = self.client.post(
            '/users/token/',
            {'email': 'test@test.com', 'password': "1234"}
        )
        self.access_token = response.json().get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        self.data = {
            'number': 1,
            'name': 'Test',
            'description': 'Test description',
        }

    def test_create_module(self):
        response = self.client.post(
            reverse('modules:module_create'),
            self.data
        )
        pk = Module.objects.all().latest('pk').pk
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.json(),
            {
                "id": pk,
                "number": 1,
                "name": "Test",
                "description": "Test description",
                "owner": self.user.pk
            }
        )

    def test_list_modules(self):
        self.test_create_module()
        response = self.client.get(reverse('modules:modules'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json()['results'],
            [
                {
                    "id": response.json()['results'][0]['id'],
                    "number": 1,
                    "name": "Test",
                    "description": "Test description",
                    "owner": self.user.pk
                }
            ]
        )

    def test_retrieve_module(self):
        self.test_create_module()
        pk = Module.objects.all().latest('pk').pk
        response = self.client.get(f'/modules/{pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "id": pk,
                "number": 1,
                "name": "Test",
                "description": "Test description",
                "owner": self.user.pk
            }
        )

    def test_update_module(self):
        self.test_create_module()
        pk = Module.objects.all().latest('pk').pk
        response = self.client.patch(f'/modules/update/{pk}/', {'name': 'Test changed'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "id": pk,
                "number": 1,
                "name": "Test changed",
                "description": "Test description",
                "owner": self.user.pk
            }
        )

    def test_destroy_module(self):
        self.test_create_module()
        pk = Module.objects.all().latest('pk').pk
        response = self.client.delete(f'/modules/delete/{pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
