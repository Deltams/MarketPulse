from django.test import TestCase
from django.db import IntegrityError
from django.contrib.auth.models import User
from ...models import Cart, Product, CartItem, User
from ..Bakery import user_recipe, cart_recipe, minimal_product_recipe, cart_item_recipe

class CartItemModelTest(TestCase):


    @classmethod
    def setUpTestData(cls):
        """Создание тестовых данных"""

        cls.user = user_recipe.make()

        cls.cart = cart_recipe.make(user=cls.user)

        cls.product = minimal_product_recipe.make()

        cls.product2 = minimal_product_recipe.make()
        
        
        cls.cart_item = cart_item_recipe.make(
            cart=cls.cart,
            product=cls.product
        )


    def test_cart_item_creation(self):
        """Тест создания элемента корзины"""

        self.assertEqual(self.cart_item.cart, self.cart)
        self.assertEqual(self.cart_item.product, self.product)


    def test_cart_relation(self):
        """Тест связи с корзиной"""

        cart = self.cart_item._meta.get_field('cart')
        self.assertEqual(cart.remote_field.model, Cart)
        self.assertEqual(cart.remote_field.on_delete.__name__, 'CASCADE')
        self.assertFalse(cart.null)
        self.assertFalse(cart.blank) 

    def test_multiple_items_per_cart(self):
        """Тест добавления несольких товаров в одну корзину"""

        CartItem.objects.create(
            cart=self.cart,
            product=self.product2
        )
        self.assertEqual(self.cart.cartitem_set.count(), 2)