from django.test import TestCase
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from ...models import UserProfile
from core.tests.runners import get_db_test   

class UserProfileModelTest(TestCase):
    databases = get_db_test()

    @classmethod
    def setUpTestData(cls):
        """Создание тестовых данных"""
        db_alias = next(iter(cls.databases))

        cls.user = User.objects.db_manager(db_alias).create_user(
            username='testuser',
            email='test@gmail.com',
            password='pass1234'
        )
        cls.user_profile = UserProfile.objects.db_manager(db_alias).create(user=cls.user)


    def test_user_profile_creation(self):
        """Тест создания профиля пользователя"""

        self.assertEqual(self.user_profile.user.username, 'testuser')
        self.assertEqual(self.user_profile.user.email, 'test@gmail.com')


    def test_one_to_one_relation_user(self):
        """Тест связи один-к-одному с пользователем"""
        db_alias = next(iter(self.databases))

        user = self.user_profile._meta.get_field('user')
        self.assertEqual(user.remote_field.model, User)
        self.assertEqual(user.remote_field.on_delete.__name__, 'CASCADE')

        with self.assertRaises(IntegrityError):
            try:
                with transaction.atomic(using=db_alias):
                    UserProfile.objects.db_manager(db_alias).create(
                        user = self.user
                    )
            except IntegrityError:
                raise
        
        self.assertEqual(UserProfile.objects.db_manager(db_alias).count(), 1)


    def test_str_representation(self):
        """Тест строкового представления"""

        self.assertEqual(str(self.user_profile), 'testuser')    