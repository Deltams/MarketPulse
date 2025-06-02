from rest_framework.test import APITestCase
from rest_framework import status
from ...models import UserProfile
from django.contrib.auth.models import User
from ..Bakery import user_profile_recipe, user_recipe



class UserProfileAPITest(APITestCase):
    

    @classmethod
    def setUpTestData(cls):
        """Создание тестовых данных"""

        cls.user1 = user_recipe.make()
        cls.first_user_profile = user_profile_recipe.make(user = cls.user1)

        cls.user2 = user_recipe.make()
        cls.second_user_profile = user_profile_recipe.make(user = cls.user2)



    def test_get_userprofile_list(self):
        """Тест GET для url /api/v1/userprofilelist/"""

        response = self.client.get('/api/v1/userprofilelist/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['user'], self.user1.id)
        self.assertEqual(response.data[1]['user'], self.user2.id)
