from django.test import TestCase
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from ...models import User, Cart
from ..Bakery import user_recipe, cart_recipe

class CartModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Создание тестовых данных"""

        cls.user = user_recipe.make()

        cls.cart = cart_recipe.make(user=cls.user)


    def test_cart_creation(self):
        """Тест создания корзины"""

        self.assertEqual(self.cart.user, self.user)

    def test_one_to_one_relation_user_profile(self):
        """Тест связи один-к-одному с профилем пользователя"""

        user = self.cart._meta.get_field('user')
        self.assertEqual(user.remote_field.model, User)
        self.assertEqual(user.remote_field.on_delete.__name__, 'CASCADE')
        self.assertTrue(user.null)
        self.assertTrue(user.blank)

        with self.assertRaises(IntegrityError):
            try:
                with transaction.atomic():
                    cart_recipe.make(
                        user=self.user
                    )
            except IntegrityError:
                raise
        
        self.assertEqual(Cart.objects.count(), 1)