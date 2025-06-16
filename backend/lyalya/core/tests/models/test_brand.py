from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from ...models import User, Brand
from ..Bakery import user_recipe, full_brand_recipe, minimal_brand_recipe


class BrandModelTest(TestCase):
    

    @classmethod
    def setUpTestData(cls):
        """Создание тестовых данных"""

        cls.user = user_recipe.make()
        
        cls.brand = full_brand_recipe.make(
            owner=cls.user,
            name='Test Brand',
            slug='test-brand',
            description='Test description',
            is_verified=True
        )


    def test_brand_creation(self):
        """Тест создания бренда"""

        self.assertEqual(self.brand.name, 'Test Brand')
        self.assertEqual(self.brand.slug, 'test-brand')
        self.assertEqual(self.brand.description, 'Test description')
        self.assertTrue(self.brand.is_verified)
        self.assertEqual(self.brand.owner, self.user)


    def test_many_to_one_relation_owner(self):
        """Тест связи многие-к-одному с владельцем"""

        owner = self.brand._meta.get_field('owner')
        self.assertEqual(owner.remote_field.model, User)
        self.assertEqual(owner.remote_field.on_delete.__name__, 'CASCADE')
        self.assertFalse(owner.null)
        self.assertFalse(owner.blank)

        # Test that a user can own multiple brands
        second_brand = full_brand_recipe.make(
            owner=self.user,
            name='Second Brand',
            slug='second-brand'
        )
        self.assertEqual(Brand.objects.filter(owner=self.user).count(), 2)
        self.assertEqual(second_brand.owner, self.user)


    def test_str_representation(self):
        """Тест строкового представления"""

        self.assertEqual(str(self.brand), 'Test Brand')


    def test_unique_name(self):
        """Тест уникальности названия бренда"""

        with self.assertRaises(IntegrityError):
           minimal_brand_recipe.make(
                name="Test Brand"
            )


    def test_max_len_name(self):
        """Тест максимальной длины названия бренда"""

        max_len = self.brand._meta.get_field('name').max_length
        self.assertEqual(max_len, 255)


    def test_unique_slug(self):
        """Тест уникальности slug"""

        with self.assertRaises(IntegrityError):
           minimal_brand_recipe.make(
                slug="test-brand"
            )


    def test_max_len_slug(self):
        """Тест максимальной длины slug"""

        max_len = self.brand._meta.get_field('slug').max_length
        self.assertEqual(max_len, 255)


    def test_optional_description(self):
        """Тест необязательного поля описание"""

        new_brand = minimal_brand_recipe.make()
        self.assertIsNone(new_brand.description)


    def test_default_value_is_verified(self):
        """Тест значения по умолчанию для поля is_verified"""

        new_brand = minimal_brand_recipe.make()
        self.assertFalse(new_brand.is_verified)