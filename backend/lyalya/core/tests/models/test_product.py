from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from ...models import Category, Brand, Product
from ..Bakery import minimal_brand_recipe, full_product_recipe, minimal_category_recipe, minimal_product_recipe, user_recipe, user_profile_recipe

class ProductModelTest(TestCase):


    @classmethod
    def setUpTestData(cls):
        """Создание тестовых данных"""

        cls.user = user_recipe.make(username=('Seller'))

        cls.seller = user_profile_recipe.make(user = cls.user)

        cls.brand = minimal_brand_recipe.make()

        cls.category = minimal_category_recipe.make()

        cls.product = full_product_recipe.make(
            brand = cls.brand,
            category = cls.category,
            name = 'Test Product',
            slug = 'test-product',
            description = 'test description',
            price = 100.99,
            is_active = False,
            seller = cls.seller
        )


    def test_product_creation(self):
        """Тест создания продукта"""

        self.assertEqual(self.product.brand, self.brand)
        self.assertEqual(self.product.category, self.category)
        self.assertEqual(self.product.name, 'Test Product')
        self.assertEqual(self.product.slug, 'test-product')
        self.assertEqual(self.product.description, 'test description')
        self.assertEqual(self.product.price, 100.99)
        self.assertEqual(self.product.is_active, False)
        self.assertEqual(self.product.seller, self.seller)
        # self.assertEqual(self.image)


    # def test_seller_relation(self):
    #     """Тест связи с продавцом"""

    #     seller = self.product._meta.get_field('brand')
    #     self.assertEqual(seller.remote_field.model, Brand)
    #     self.assertEqual(seller.remote_field.on_delete.__name__, 'CASCADE')


    def test_brand_relation(self):
        """Тест связи с брендом"""

        brand = self.product._meta.get_field('brand')
        self.assertEqual(brand.remote_field.model, Brand)
        self.assertEqual(brand.remote_field.on_delete.__name__, 'CASCADE')
        self.assertTrue(brand.null)
        self.assertTrue(brand.blank)


    def test_category_relation(self):
        """Тест связи с категорией"""

        category = self.product._meta.get_field('category')
        self.assertEqual(category.remote_field.model, Category)
        self.assertEqual(category.remote_field.on_delete.__name__, 'SET_NULL')
        self.assertTrue(category.null)
        self.assertTrue(category.blank)


    def test_max_len_name(self):
        """Тест максимальной длины названия продукта"""

        max_len = self.product._meta.get_field('name').max_length
        self.assertEqual(max_len, 255)


    def test_max_len_slug(self):
        """Тест максимальной длины slug"""

        max_len = self.product._meta.get_field('slug').max_length
        self.assertEqual(max_len, 255)


    def test_unique_slug(self):
        """Тест уникальности slug"""

        with self.assertRaises(IntegrityError):
            minimal_product_recipe.make(
                slug = "test-product"
            )


    def test_optional_fields(self):
        """Тест необязательных полей"""

        new_product = minimal_product_recipe.make()

        self.assertIsNone(new_product.brand)
        self.assertIsNone(new_product.category)
        self.assertIsNone(new_product.description)


    def test_default_value_is_active(self):
        """Тест значения по умолчанию для поля is_active"""

        new_product = minimal_product_recipe.make()
        self.assertTrue(new_product.is_active)


    def test_price_max_digits(self):
        """Тест максимального количества цифр для цены"""
        
        max_digits = self.product._meta.get_field('price').max_digits
        self.assertEqual(max_digits, 10)


    def test_price_decimal_places(self):
        """Тест количества знаков после запятой для цены"""

        decimal_places = self.product._meta.get_field('price').decimal_places
        self.assertEqual(decimal_places, 2)


    def test_max_price_value(self):
        """Тест максимальной цены"""

        product = minimal_product_recipe.make(
            price = 9999999.99
        )
        self.assertEqual(product.price, 9999999.99)


    def test_negative_price(self):
        """Тест отрицательной цены"""

        with self.assertRaises(ValidationError):
            minimal_product_recipe.make(
                price = -10.00
            )    