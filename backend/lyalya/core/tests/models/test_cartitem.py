from django.test import TestCase
from django.db import IntegrityError
from django.contrib.auth.models import User
from ...models import Cart, Product, CartItem, UserProfile
from decimal import Decimal
from core.tests.runners import get_db_test

class CartItemModelTest(TestCase):
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

        cls.product = Product.objects.db_manager(db_alias).create(
            name='Test Product',
            slug='test-product',
            price=Decimal('10.00')
        )

        cls.product2 = Product.objects.db_manager(db_alias).create(
            name='Test Product2',
            slug='test-product2',
            price=Decimal('99.00')
        )
        
        cls.cart_item = CartItem.objects.db_manager(db_alias).create(
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


    def test_product_relation(self):
        """Тест связи с товаром"""

        product = self.cart_item._meta.get_field('product')
        self.assertEqual(product.remote_field.model, Product)
        self.assertEqual(product.remote_field.on_delete.__name__, 'CASCADE')
        self.assertFalse(product.null)
        self.assertFalse(product.blank) 


    def test_multiple_items_per_cart(self):
        """Тест добавления несольких товаров в одну корзину"""
        db_alias = next(iter(self.databases))

        CartItem.objects.db_manager(db_alias).create(
            cart=self.cart,
            product=self.product2
        )
        self.assertEqual(self.cart.cartitem_set.count(), 2)