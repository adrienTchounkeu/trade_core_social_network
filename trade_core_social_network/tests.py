from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from .models import User, Post


class UserTestCase(APITestCase):
    def test_create_account(self):
        """
        Ensure we can create a user
        :return:
        """

        url = reverse('user')
        data = {'email': 'adrientchounkeu10@gmail.com', 'password': 'asdfds8653468'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().geolocation_data_country, 'country')

    def test_retrieve_account(self):
        """
        Ensure we can retrieve user data
        :return:
        """
        url = reverse('user')
        data = {'email': 'adrientchounkeu10@gmail.com'}
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.data['geolocation_data_country'], 'country')


class PostTestCase(APITestCase):
    def test_create_post(self):
        """
        Ensure we can create a user
        :return:
        """

        url = reverse('post')
        data = {'email': 'adrientchounkeu10@gmail.com', 'text': 'Hello World'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.get().creator.email, 'adrientchounkeu10@gmail.com')

    def test_retrieve_account(self):
        """
        Ensure we can retrieve user data
        :return:
        """
        url = reverse('post')
        data = {'id_post': 0}
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(response.data['text'], 'Hello World')
        creator_email = response.data['creator']
        user = User.objects.get(pk=creator_email)
        self.assertEqual(user.email, 'adrientchounkeu10@gmail.com')
        self.assertEqual(user.geolocation_data_country, 'country')
