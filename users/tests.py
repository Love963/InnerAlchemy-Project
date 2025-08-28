from django.test import TestCase, Client
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class UsersAPITestCase(TestCase):

    def setUp(self):
        self.client = Client()            # For web client tests
        self.api_client = APIClient()     # For API tests

        # Create regular user
        self.user = User.objects.create_user(
            email='user@example.com',
            username='user',
            password='userpass',
            first_name='Regular',
            last_name='User'
        )

        # Create admin user
        self.admin = User.objects.create_superuser(
            email='admin@example.com',
            username='admin',
            password='adminpass'
        )

    # Web Client Tests
    def test_login_logout_web_client(self):
        # Login with email
        login = self.client.login(email='user@example.com', password='userpass')
        self.assertTrue(login)

        # Access profile page
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 200)

        # Logout
        self.client.logout()
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 302)  # redirect to login

    # API Tests
    def test_register_user_api(self):
        url = reverse('users:api-register')
        data = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'password': 'strongpass123',
            'first_name': 'New',
            'last_name': 'User'
        }
        response = self.api_client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email='newuser@example.com').exists())

    def test_profile_retrieve_update_authenticated(self):
        url = reverse('users:api-me')
        self.api_client.force_authenticate(user=self.user)

        # Retrieve
        response = self.api_client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)

        # Partial Update using PATCH
        response = self.api_client.patch(url, {'first_name': 'UpdatedName'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'UpdatedName')

    # Admin-only API Tests
    def test_user_list_admin_only(self):
        url = reverse('users:api-user-list')

        # Regular user cannot access
        self.api_client.force_authenticate(user=self.user)
        response = self.api_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Admin can access
        self.api_client.force_authenticate(user=self.admin)
        response = self.api_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 2)

    def test_user_detail_admin_only(self):
        url = reverse('users:api-user-detail', args=[self.user.id])

        # Regular user cannot access
        self.api_client.force_authenticate(user=self.user)
        response = self.api_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Admin can access
        self.api_client.force_authenticate(user=self.admin)
        response = self.api_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)
