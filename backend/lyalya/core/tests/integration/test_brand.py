from rest_framework.test import APITestCase
from rest_framework import status
from ..Bakery import full_product_recipe, full_brand_recipe, user_recipe
from ...models import Brand

class BrandIntegrationTest(APITestCase):
    

    @classmethod
    def setUpTestData(cls):
        """Создание тестовых данных"""

        cls.user = user_recipe.make(username='test-owner', is_seller=True)

        cls.first_brand = full_brand_recipe.make(
            name='First Brand',
            slug='first-brand',
            owner=cls.user,
            is_verified=True
        )

        cls.second_brand = full_brand_recipe.make(
            name='Second Brand',
            slug='second-brand'
        )

        cls.first_product = full_product_recipe.make(
            name='First Product',
            slug='first-product',
            brand=cls.first_brand
        )
        
        cls.second_product = full_product_recipe.make(
            name='Second Product',
            slug='second-product',
            brand=None
        )



    # def test_brand_owner(self):
    #     """Тест отображения брендом своего владельца"""

    #     brand_url = f'/api/v1/brandlist/{self.first_brand.id}/'
    #     brand_response = self.client.get(brand_url)

    #     self.assertEqual(brand_response.status_code, 200)
    #     owner_id = brand_response.data['owner']

    #     profile_url = f'/api/v1/userprofilelist/{owner_id}/'
    #     profile_response = self.client.get(profile_url)

    #     self.assertEqual(profile_response.status_code, 200) 
    #     self.assertEqual(profile_response.data['user'], self.userprofile.user)


    # def test_brand_deletion_with_products(self):
    #     """Попытка удаления бренда с привязанными продуктами должна вызывать ошибку"""
    #     response = self.client.delete(f'/api/v1/brandlist/{self.first_brand.id}/')
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertTrue(Brand.objects.filter(id=self.first_brand.id).exists())


