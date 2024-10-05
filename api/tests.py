from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from .models import *
from .serializers import *

# Create your tests here.

# Create Task Test
class CreateTaskViewTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = reverse('create_task') 
        self.valid_payload = {
            'title': 'Test Task',
            'description': 'Test Task Description',
           
        }
        self.invalid_payload = {
            'title': '',
            'description': '',
        }

    def test_create_task_success(self):
        response = self.client.post(self.url, data=self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Task Created Successfully')

        task = TaskModel.objects.get(title='Test Task')
        self.assertIsNotNone(task)

    def test_create_task_failure(self):
        response = self.client.post(self.url, data=self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data)  
        self.assertIn('description', response.data)


# Test Update Delete and task by Id
class TaskDetailViewTest(APITestCase):

    def setUp(self):
        self.client = APIClient()

        self.task = TaskModel.objects.create(
            title='Sample Task',
            description='Sample Task Description',
           
        )
        self.valid_payload = {
            'title': 'Updated Task',
            'description': 'Updated Task Description',
            
        }
        self.invalid_payload = {
            'title': '',
            'description': ''
        }
        self.detail_url = reverse('task_detail', kwargs={'task_id': self.task.id})

    def test_get_task_success(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Successfully")
        self.assertEqual(response.data['data']['title'], 'Sample Task')

    def test_get_task_not_found(self):
        invalid_detail_url = reverse('task_detail', kwargs={'task_id': 9999})
        response = self.client.get(invalid_detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Task not found')

    def test_update_task_success(self):
        response = self.client.put(self.detail_url, data=self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Task Updated Successfully')
        self.assertEqual(response.data['data']['title'], 'Updated Task')

    def test_update_task_invalid(self):
        response = self.client.put(self.detail_url, data=self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data)  

    def test_delete_task_success(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Task Deleted Successfully')

    def test_delete_task_not_found(self):
        invalid_detail_url = reverse('task_detail', kwargs={'task_id': 9999})
        response = self.client.delete(invalid_detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Task not found')


# Test All Task
class TaskListViewTest(APITestCase):

    def setUp(self):
        self.client = APIClient()

        self.list_url = reverse('task_list')

        self.task1 = TaskModel.objects.create(
            title='Task 1',
            description='Description for task 1',
           
        )
        self.task2 = TaskModel.objects.create(
            title='Task 2',
            description='Description for task 2',
    

        )

    def test_get_all_tasks(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 200)
        self.assertEqual(response.data['message'], "Successfully")
        self.assertEqual(len(response.data['data']), 2)  

    def test_get_no_tasks(self):
        TaskModel.objects.all().delete()
        response = self.client.get(self.list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 200)
        self.assertEqual(response.data['message'], "Successfully")
        self.assertEqual(len(response.data['data']), 0)  


