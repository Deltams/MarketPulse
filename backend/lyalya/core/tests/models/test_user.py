from django.test import TestCase
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from ...models import User
from ..Bakery import user_recipe

class UserModelTest(TestCase):

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


    def test_user_creation(self):
        """Тест создания пользователя"""

        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@gmail.com')
        self.assertEqual(self.user.is_seller, True )
        self.assertEqual(self.user.is_buyer, False )


    def test_unique_email(self):
        """Тест уникальности email"""

        with self.assertRaises(IntegrityError):
           user_recipe.make(
                email="test@gmail.com"
            )
           

    def test_default_values(self):
        """Тест значений по умолчанию"""

        new_user = user_recipe.make()

        self.assertFalse(new_user.is_seller)
        self.assertTrue(new_user.is_buyer)

           
    def test_str_representation(self):
        """Тест строкового представления"""

        self.assertEqual(str(self.user),'test@gmail.com')



  