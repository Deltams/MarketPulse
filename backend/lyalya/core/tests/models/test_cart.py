from django.test import TestCase
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from ...models import UserProfile, Cart
from ..Bakery import user_profile_recipe, cart_recipe

class CartModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Создание тестовых данных"""

        cls.user_profile = user_profile_recipe.make()

        cls.cart = cart_recipe.make(user = cls.user_profile)


    def test_cart_creation(self):
        """Тест создания корзины"""

        self.assertEqual(self.cart.user, self.user_profile)

    def test_one_to_one_relation_user_profile(self):
        """Тест связи один-к-одному с профилем пользователя"""

        user_profile = self.cart._meta.get_field('user')
        self.assertEqual(user_profile.remote_field.model, UserProfile)
        self.assertEqual(user_profile.remote_field.on_delete.__name__, 'CASCADE')
        self.assertFalse(user_profile.null)
        self.assertFalse(user_profile.blank)

        with self.assertRaises(IntegrityError):
            try:
                with transaction.atomic():
                    cart_recipe.make(
                        user = self.user_profile
                    )
            except IntegrityError:
                raise
        
        self.assertEqual(Cart.objects.count(), 1)