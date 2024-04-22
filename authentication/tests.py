from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.conf import settings
from .models import Account  # Adjust the import path according to your project structure
from django.contrib.auth import get_user_model



class LoginViewTestCase(TestCase):
    def setUp(self):
        # Create a custom user for authentication using your Account model
        self.user = Account.objects.create_user(email='test@example.com', username='testuser', password='password123')
        self.client = APIClient()

    def test_successful_login(self):
        # Endpoint for the login view
        url = reverse('authentication:login_url') 
        data = {'email': 'test@example.com', 'password': 'password123'}
        
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check if the cookies are set properly
        self.assertIn(settings.SIMPLE_JWT['AUTH_COOKIE'], response.cookies)
        self.assertIn(settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'], response.cookies)
        self.assertIn('X-CSRFToken', response)

    def test_failed_login(self):
        url = reverse('authentication:login_url')  # Again, replace 'login_url_name' with the actual name of your login URL
        data = {'email': 'wrong@example.com', 'password': 'wrongpassword'}
        
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  # or the status code you expect on failure

# More tests can be added as necessary, such as checking for the correct response structure, additional headers, etc.

User = get_user_model()

class RegisterViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('authentication:register')  # Adjust 'authentication:register' to match your register URL's name
    
    def test_successful_registration(self):
        data = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'password': 'testpassword123',
            'password2':'testpassword123'
        }
        
        response = self.client.post(self.url, data, format='json')
        
        # Check that the response indicates success
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "Registered!")
        
        # Verify the user was created in the database
        self.assertTrue(User.objects.filter(email='newuser@example.com').exists())
        
    def test_failed_registration_with_invalid_data(self):
        data = {
            'email': 'notanemail',  # Invalid email format
            'username': '',  # Empty username
            'password': 'short',  # Potentially invalid password (too short or does not meet criteria)
            # Any other fields can be omitted or filled with invalid data
        }
        
        response = self.client.post(self.url, data, format='json')
        
        # Assuming your serializer and view properly validate data and return a 400 Bad Request for invalid data
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(first=response.data['username'][0].code, second='blank')
        self.assertEqual(first=response.data['password'][0].code, second='password_too_short')
        self.assertEqual(first=response.data['email'][0].code, second='invalid')


