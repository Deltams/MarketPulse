from django.test import TestCase
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from ...models import UserProfile, Cart
from core.tests.runners import get_db_test

class CartModelTest(TestCase):
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

        cls.cart = Cart.objects.db_manager(db_alias).create(user = cls.user_profile)


    def test_cart_creation(self):
        """Тест создания корзины"""

        self.assertEqual(self.cart.user, self.user_profile)

    def test_one_to_one_relation_user_profile(self):
        """Тест связи один-к-одному с профилем пользователя"""
        db_alias = next(iter(self.databases))

        user_profile = self.cart._meta.get_field('user')
        self.assertEqual(user_profile.remote_field.model, UserProfile)
        self.assertEqual(user_profile.remote_field.on_delete.__name__, 'CASCADE')
        self.assertFalse(user_profile.null)
        self.assertFalse(user_profile.blank)

        with self.assertRaises(IntegrityError):
            try:
                with transaction.atomic(using=db_alias):
                    Cart.objects.db_manager(db_alias).create(
                        user = self.user_profile
                    )
            except IntegrityError:
                raise
        
        self.assertEqual(Cart.objects.db_manager(db_alias).count(), 1)