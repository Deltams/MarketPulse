from django.test import TestCase
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from ...models import UserProfile   

class UserProfileModelTest(TestCase):
 
    @classmethod
    def setUpTestData(cls):
        """Создание тестовых данных"""

        cls.user = User.objects.create_user(
            username='testuser',
            email='test@gmail.com',
            password='pass1234'
        )
        cls.user_profile = UserProfile.objects.create(user=cls.user)


    def test_user_profile_creation(self):
        """Тест создания профиля пользователя"""

        self.assertEqual(self.user_profile.user.username, 'testuser')
        self.assertEqual(self.user_profile.user.email, 'test@gmail.com')


    def test_one_to_one_relation_user(self):
        """Тест связи один-к-одному с пользователем"""

        user = self.user_profile._meta.get_field('user')
        self.assertEqual(user.remote_field.model, User)
        self.assertEqual(user.remote_field.on_delete.__name__, 'CASCADE')

        with self.assertRaises(IntegrityError):
            try:
                with transaction.atomic():
                    UserProfile.objects.create(
                        user = self.user
                    )
            except IntegrityError:
                raise
        
        self.assertEqual(UserProfile.objects.count(), 1)


    def test_str_representation(self):
        """Тест строкового представления"""

        self.assertEqual(str(self.user_profile), 'testuser')


    