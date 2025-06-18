from django.test import TestCase
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from ...models import User, SellerProfile
from ..Bakery import user_recipe, seller_profile_recipe

class SellerProfileModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Создание тестовых данных"""

        cls.user = user_recipe.make(
            username='testuser',
            email='test@gmail.com',
            password='pass1234',
            is_seller=True
        )

        cls.seller_profile = seller_profile_recipe.make(
            user=cls.user,
            business_name= 'Business',
            slug = 'business',
            description='Business Description',
            is_verified = True
            )


    def test_seller_profile_creation(self):
        """Тест создания профиля продавца"""

        self.assertEqual(self.seller_profile.user.username, 'testuser')
        self.assertEqual(self.seller_profile.user.email, 'test@gmail.com')
        self.assertTrue(self.seller_profile.user.is_seller)
        self.assertEqual(self.seller_profile.business_name, 'Business')
        self.assertEqual(self.seller_profile.slug, 'business')
        self.assertEqual(self.seller_profile.description, 'Business Description')
        self.assertEqual(self.seller_profile.is_verified, True)


    def test_one_to_one_relation_user(self):
        """Тест связи один-к-одному с пользователем"""

        user = self.seller_profile._meta.get_field('user')
        self.assertEqual(user.remote_field.model, User)
        self.assertEqual(user.remote_field.on_delete.__name__, 'CASCADE')

        with self.assertRaises(IntegrityError):
            try:
                with transaction.atomic():
                    seller_profile_recipe.make(
                        user=self.user
                    )
            except IntegrityError:
                raise
        
        self.assertEqual(SellerProfile.objects.count(), 1)



    def test_max_len_name(self):
        """Тест максимальной длины названия бизнеса"""

        max_len = self.seller_profile._meta.get_field('business_name').max_length
        self.assertEqual(max_len, 255)


    def test_unique_slug(self):
        """Тест уникальности slug"""

        with self.assertRaises(IntegrityError):
           seller_profile_recipe.make(
                slug="business"
            )


    def test_max_len_slug(self):
        """Тест максимальной длины slug"""

        max_len = self.seller_profile._meta.get_field('slug').max_length
        self.assertEqual(max_len, 255)


    def test_optional_description(self):
        """Тест необязательного поля описание"""

        new_brand = seller_profile_recipe.make(description = None)
        self.assertIsNone(new_brand.description)


    def test_default_value_is_verified(self):
        """Тест значения по умолчанию для поля is_verified"""

        new_brand = seller_profile_recipe.make()
        self.assertTrue(new_brand.is_verified)


    def test_str_representation(self):
        """Тест строкового представления"""

        self.assertEqual(str(self.seller_profile),'Business')
