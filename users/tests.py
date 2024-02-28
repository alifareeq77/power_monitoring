# users/tests.py
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

class UserCreationLoginLogoutTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_user_creation(self):
        # Test user creation
        response = self.client.post(reverse('register'), {
            'email': 'test@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
        })
        self.assertEqual(response.status_code, 302)  # Check if the user is redirected after successful registration
        self.assertTrue(get_user_model().objects.filter(email='test@example.com').exists())  # Check if the user exists in the database

    def test_user_login_logout(self):
        # Create a user
        user = get_user_model().objects.create_user(email='test@example.com', password='testpassword')

        # Test user login
        login_response = self.client.post(reverse('login'), {
            'username': 'test@example.com',
            'password': 'testpassword',
        })
        self.assertEqual(login_response.status_code, 302)  # Check if the user is redirected after successful login

        # Test user logout
        logout_response = self.client.get(reverse('logout'))
        self.assertEqual(logout_response.status_code, 302)  # Check if the user is redirected after logout
        self.assertFalse('_auth_user_id' in self.client.session)  # Check if the user is logged out (session should not contain '_auth_user_id')

    def test_user_login_invalid_credentials(self):
        # Test user login with invalid credentials
        response = self.client.post(reverse('login'), {
            'username': 'test@example.com',
            'password': 'invalidpassword',
        })
        self.assertEqual(response.status_code, 200)  # Check if the login page is rendered again
        self.assertFalse('_auth_user_id' in self.client.session)  # Check if the user is not logged in (session should not contain '_auth_user_id')


class SuperuserCreationTestCase(TestCase):
    def test_superuser_creation(self):
        User = get_user_model()
        # Create a superuser
        User.objects.create_superuser(email='admin@example.com', password='adminpassword')

        # Check if the superuser exists in the database
        superuser = User.objects.get(email='admin@example.com')
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)