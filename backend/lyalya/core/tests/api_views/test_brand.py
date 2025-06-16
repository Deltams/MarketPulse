from rest_framework.test import APITestCase
from rest_framework import status
from ..Bakery import full_brand_recipe, user_recipe
from ...models import Brand


class BrandAPITest(APITestCase):
    

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



    def test_get_brand_list(self):
        """Тест GET для списка брендов url api/v1/brandlist/"""

        url = '/api/v1/brandlist/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], 'First Brand')
        self.assertEqual(response.data[1]['name'], 'Second Brand')


    def test_get_brand_detail(self):
        """Тест GET для детальной информации о бренде url api/v1/brandlist/<int:pk>/"""

        url = f'/api/v1/brandlist/{self.first_brand.id}/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'First Brand')
        self.assertEqual(response.data['slug'], 'first-brand')
        self.assertEqual(response.data['is_verified'], True)


    def test_post_brand_list(self):
        """Тест POST для создания бренда url api/v1/brandlist/"""

        self.client.force_authenticate(user=self.user)

        url = '/api/v1/brandlist/'
        data = {
            'name': 'New Brand',
            'slug': 'new-brand',
            'description': 'New Brand Description',
            'is_verified': False
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], 'New Brand')
        self.assertEqual(response.data['slug'], 'new-brand')
        self.assertEqual(response.data['is_verified'], False)


    def test_put_brand_detail(self):
        """Тест PUT для обновления бренда url api/v1/brandlist/<int:pk>/"""

        self.client.force_authenticate(user=self.user)

        url = f'/api/v1/brandlist/{self.first_brand.id}/'
        data = {
            'name': 'Updated Brand',
            'slug': 'updated-brand',
            'description': 'Updated Brand Description',
            'is_verified': True
        }
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Updated Brand')
        self.assertEqual(response.data['slug'], 'updated-brand')
        self.assertEqual(response.data['is_verified'], True)


    def test_delete_brand_detail(self):
        """Тест DELETE для удаления бренда url api/v1/brandlist/<int:pk>/"""

        self.client.force_authenticate(user=self.user)

        url = f'/api/v1/brandlist/{self.first_brand.id}/'
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Brand.objects.filter(id=self.first_brand.id).exists()) 