from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework.routers import reverse
from tasks.models import User, Task
from tasks.serializers import *


class LowonganListAPIViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            phone='77777777777',
            email='test@test.com',
            password='123456'
        )
        token = Token.objects.create(user=self.user).key
        self.headers = {
            'HTTP_AUTHORIZATION': f'Token {token}'
        }
        self.task = Task.objects.create(
            user=self.user,
            title='titel',
            description='description',
            execution_at=timezone.now()
        )

    def test_tasks_list(self):
        """
        Test to tasks list
        """
        response = self.client.get(reverse('todo-list'), **self.headers)
        self.assertEqual(200, response.status_code)

    def test_tasks_detail(self):
        """
        Test to tasks detail
        """
        response = self.client.get(
            reverse("todo-detail", kwargs={"pk": self.task.pk}), **self.headers)
        self.assertEqual(200, response.status_code)

        customer_serializer_data = RetrieveTaskSerializer(
            instance=self.task).data
        response_data = response.json()
        self.assertEqual(customer_serializer_data, response_data)

    def test_customers_create(self):
        """
        Test to task create
        """
        data = {
            'title': 'title',
            'description': 'description',
            'execution_at': timezone.now()
        }
        response = self.client.post(
            reverse('todo-list'), data=data, **self.headers)
        self.assertEqual(201, response.status_code)
        task_created = Task.objects.filter(
            pk=response.json()['id']).exists()
        self.assertTrue(task_created)

    def test_customers_update(self):
        """
        Test to task update
        """
        data = {
            'title': 'new title',
        }
        response = self.client.patch(
            reverse('todo-detail', kwargs={"pk": self.task.pk}), data=data, **self.headers)
        self.assertEqual(200, response.status_code)
        task = Task.objects.get(pk=self.task.pk)
        self.assertEqual(task.title, data['title'])
