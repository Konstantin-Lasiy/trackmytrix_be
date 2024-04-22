from django.test import TestCase

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import DailyWeight

User = get_user_model()


class URLsTestCase(APITestCase):
    def test_reverse_hello_world(self):
        url = reverse('myapi:hello_world')
        self.assertEqual(url, '/api/hello-world/')

class WeightEntryTestCase(APITestCase):

    def setUp(self):
        # Create two users
        self.user1 = User.objects.create_user(username='user1', email='test@test.com', password='pass1')
        self.user2 = User.objects.create_user(username='user2', email='test2@test.com', password='pass2')
        
        # Create weight entries for user1
        self.weight_entry = DailyWeight.objects.create(user=self.user1, date='2023-04-14', weight=70.0)

        # URL for getting and posting entries
        self.url_list_create = reverse('myapi:weight_entries')

        # URL for retrieving, updating, and deleting a specific entry
        self.url_detail = reverse('myapi:weight_entry_detail', kwargs={'pk': self.weight_entry.id})

    def test_list_entries(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(self.url_list_create)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Ensure only user1's entry is returned

    def test_create_entry(self):
        self.client.force_authenticate(user=self.user1)
        data = {'date': '2023-04-15', 'weight': 68.5}
        response = self.client.post(self.url_list_create, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DailyWeight.objects.count(), 2)

    def test_retrieve_entry(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['weight'], '70.00')  # Check that the correct weight is retrieved

    def test_update_entry(self):
        self.client.force_authenticate(user=self.user1)
        data = {'date': '2023-04-14', 'weight': 69.0}
        response = self.client.put(self.url_detail, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.weight_entry.refresh_from_db()
        self.assertEqual(self.weight_entry.weight, 69.0)

    def test_delete_entry(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(DailyWeight.objects.count(), 0)

    def test_unauthorized_access(self):
        self.client.force_authenticate(user=self.user2)
        # User2 should not be able to access User1's entry
        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
