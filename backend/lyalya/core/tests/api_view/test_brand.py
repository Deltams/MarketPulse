from rest_framework.test import APITestCase
from rest_framework import status
from ...models import Brand
from ..Bakery import minimal_brand_recipe

class BrandAPITest(APITestCase):
    

    @classmethod
    def setUpTestData(cls):
        """Создание тестовых данных"""

        cls.first_brand = minimal_brand_recipe.make(
            name='First Brand',
            slug='first-brand'
        )
        
        cls.second_brand = minimal_brand_recipe.make(
            name='Second Brand',
            slug='second-brand'
        )


    def test_get_brand_list(self):
        """Тест GET для url /api/v1/brandlist/"""

        response = self.client.get('/api/v1/brandlist/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['name'], 'First Brand')
        self.assertEqual(response.data[1]['name'], 'Second Brand')


    def test_get_brand_detail(self):
        """Тест GET для url api/v1/brandlist/<int:pk>/"""

        url = f'/api/v1/brandlist/{self.first_brand.id}/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'First Brand')

    
    def test_get_brand_detail_by_non_existent_id(self):
        """Тест для url GET api/v1/brandlist/<int:pk>/ с несуществующим id"""

        non_existent_id = 99999
        url = f'/api/v1/brandlist/<int:pk>/{non_existent_id}/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)



    