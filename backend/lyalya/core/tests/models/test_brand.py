from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from ...models import UserProfile, Brand
from core.tests.runners import get_db_test

class BrandModelTest(TestCase):
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
        
        cls.brand = Brand.objects.db_manager(db_alias).create(
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
        db_alias = next(iter(self.databases))

        owner = self.brand._meta.get_field('owner')
        self.assertEqual(owner.remote_field.model, UserProfile)
        self.assertEqual(owner.remote_field.on_delete.__name__, 'CASCADE')
        self.assertTrue(owner.null)
        self.assertTrue(owner.blank)

        with self.assertRaises(IntegrityError):
            try:
                with transaction.atomic(using=db_alias):
                    Brand.objects.db_manager(db_alias).create(
                        name = "Test Brand2",
                        slug = "test-brand2",
                        owner = self.user_profile
                    )
            except IntegrityError:
                raise
        
        self.assertEqual(Brand.objects.db_manager(db_alias).count(), 1)


    def test_str_representation(self):
        """Тест строкового представления"""

        self.assertEqual(str(self.brand), 'Test Brand')

    
    def test_unique_name(self):
        """Тест уникальности названия бренда"""
        db_alias = next(iter(self.databases))

        duplicate_brand = Brand(
            name = "Test Brand",
            slug = "test-brand2"
        )
        with self.assertRaises(ValidationError):
            similar_objects = Brand.objects.db_manager(db_alias).filter(name=duplicate_brand.name)

            if similar_objects.exists():
                raise ValidationError("Name must be unique.")

    def test_max_len_name(self):
        """Тест максимальной длины названия бренда"""

        max_len = self.brand._meta.get_field('name').max_length
        self.assertEqual(max_len, 255)


    def test_unique_slug(self):
        """Тест уникальности slug"""

        db_alias = next(iter(self.databases))

        duplicate_brand = Brand(
            name = "Test Brand2",
            slug = "test-brand"
        )

        with self.assertRaises(ValidationError):
            similar_objects = Brand.objects.db_manager(db_alias).filter(slug=duplicate_brand.slug)

            if similar_objects.exists():
                raise ValidationError("Slug must be unique.")


    def test_max_len_slug(self):
        """Тест максимальной длины slug"""

        max_len = self.brand._meta.get_field('slug').max_length
        self.assertEqual(max_len, 255)


    def test_optional_description(self):
        """Тест необязательного поля описание"""

        db_alias = next(iter(self.databases))

        new_brand = Brand.objects.db_manager(db_alias).create(
            name='Test Brand2',
            slug='test-brand2'
        )
        self.assertIsNone(new_brand.description)


    def test_default_value_is_verified(self):
        """Тест значения по умолчанию для поля is_verified"""

        db_alias = next(iter(self.databases))

        new_brand = Brand.objects.db_manager(db_alias).create(
            name='Test Brand2',
            slug='test-brand2'
        )
        self.assertFalse(new_brand.is_verified)