from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from ..Bakery import user_recipe



class UserAPITest(APITestCase):
    

    @classmethod
    def setUpTestData(cls):
        """Создание тестовых данных"""

        cls.user = user_recipe.make(
            username='testuser',
            email='test@gmail.com',
            password='pass1234',
            is_seller=True,
            is_buyer = False
        )


    def test_register_new_user(self):
        """Тест POST нового пользователя для/api/v1/auth/register"""

        url = f'/api/v1/auth/register'

        data = {
                'email': 'newuser@gmail.com',
                'username': 'NewUser',
                'is_seller': True,
                'is_buyer': False,
                'password': 'passwordnew1234'
               }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['user']['username'], 'NewUser')
        self.assertEqual(response.data['user']['is_seller'], True)
        self.assertEqual(response.data['user']['is_buyer'], False)



    def test_register_new_user_with_existent_email(self):
        """Тест POST нового пользователя с сущ email для /api/v1/auth/register"""

        url = f'/api/v1/auth/register'

        data = {
                'email': 'test@gmail.com',
                'username': 'NewUser',
                'is_seller': True,
                'is_buyer': False,
                'password': 'passwordnew1234'
               }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, 400)


    def test_get_userprofile_by_auth_user(self):
        """Тест GET профиля авторизованного пользователя для /api/v1/auth/user/"""

        self.client.force_authenticate(user=self.user)
        
        url = f'/api/v1/auth/user/'
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)


    def test_get_userprofile_by_non_auth_user(self):
        """Тест GET профиля неавторизованного пользователя для /api/v1/auth/user/"""
        
        url = f'/api/v1/auth/user/'
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 403)
