from django.test import TestCase
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from ...models import User, BuyerProfile
from ..Bakery import user_recipe, buyer_profile_recipe


class BuyerProfileModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Создание тестовых данных"""

        cls.user = user_recipe.make(
            username='testuser',
            email='test@gmail.com',
            password='pass1234',
            is_buyer=True
        )
        cls.buyer_profile = buyer_profile_recipe.make(user=cls.user)


    def test_buyer_profile_creation(self):
        """Тест создания профиля покупателя"""

        self.assertEqual(self.buyer_profile.user.username, 'testuser')
        self.assertEqual(self.buyer_profile.user.email, 'test@gmail.com')
        self.assertEqual(self.buyer_profile.user.is_buyer, True)



    def test_one_to_one_relation_user(self):
        """Тест связи один-к-одному с пользователем"""

        user = self.buyer_profile._meta.get_field('user')
        self.assertEqual(user.remote_field.model, User)
        self.assertEqual(user.remote_field.on_delete.__name__, 'CASCADE')

        with self.assertRaises(IntegrityError):
            try:
                with transaction.atomic():
                    buyer_profile_recipe.make(
                        user=self.user
                    )
            except IntegrityError:
                raise
        
        self.assertEqual(BuyerProfile.objects.count(), 1)    