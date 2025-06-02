from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from ...models import UserProfile, Brand
from ..Bakery import user_profile_recipe, full_brand_recipe, minimal_brand_recipe


class BrandModelTest(TestCase):
    

    @classmethod
    def setUpTestData(cls):
        """Создание тестовых данных"""

        cls.user_profile = user_profile_recipe.make()
        
        cls.brand = full_brand_recipe.make(
            owner=cls.user_profile,
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
        self.assertEqual(self.brand.owner, self.user_profile)


    def test_one_to_one_relation_owner(self):
        """Тест связи один-к-одному с владельцем"""

        owner = self.brand._meta.get_field('owner')
        self.assertEqual(owner.remote_field.model, UserProfile)
        self.assertEqual(owner.remote_field.on_delete.__name__, 'CASCADE')
        self.assertTrue(owner.null)
        self.assertTrue(owner.blank)

        with self.assertRaises(IntegrityError):
            try:
                with transaction.atomic():
                    full_brand_recipe.make(
                        owner = self.user_profile
                    )
            except IntegrityError:
                raise
        
        self.assertEqual(Brand.objects.count(), 1)


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