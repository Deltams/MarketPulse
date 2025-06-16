from rest_framework.test import APITestCase
from rest_framework import status
from ...models import Brand
from ..Bakery import minimal_brand_recipe, user_recipe

class BrandAPITest(APITestCase):
    

    @classmethod
    def setUpTestData(cls):
        """Создание тестовых данных"""

        cls.user = user_recipe.make(username='test-owner', is_seller=True)

        cls.first_brand = minimal_brand_recipe.make(
            name='First Brand',
            slug='first-brand',
            owner=cls.user
        )
        
        cls.second_brand = minimal_brand_recipe.make(
            name='Second Brand',
            slug='second-brand',
            owner=cls.user
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
        url = f'/api/v1/brandlist/{non_existent_id}/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)


    def test_put_brand_detail(self):
        """Тест PUT для api/v1/brandlist/<int:pk>/"""
       
        self.client.force_authenticate(user=self.user)

        url = f'/api/v1/brandlist/{self.second_brand.id}/'

        data = {
            'name': 'Updated Brand',
            'slug': 'updated-brand',
            'owner': self.user.id
        }

        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Updated Brand')
        self.assertEqual(response.data['slug'], 'updated-brand')


    def test_patch_brand_detail(self):
        """Тест PATCH для url api/v1/brandlist/<int:pk>/"""
       
        self.client.force_authenticate(user=self.user)

        url = f'/api/v1/brandlist/{self.second_brand.id}/'

        data = { 'name': 'Patched Brand' }
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Patched Brand')
        self.assertEqual(response.data['slug'], 'second-brand')


    def test_delete_brand_detail(self):
        """Тест DELETE для url api/v1/brandlist/<int:pk>/"""

        self.client.force_authenticate(user=self.user)

        url = f'/api/v1/brandlist/{self.second_brand.id}/'
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Brand.objects.count(), 1)



    # def test_post_product_list_validation(self):
    #     """Тест валидации для api/v1/productlist/"""

    #     url = f'/api/v1/productlist/'

    #     data = {
    #             'name': 'Bad Price',
    #             'slug': 'Bad-price',
    #             'price': '-100.99'
    #             }
        
    #     response = self.client.post(url, data, format='json')
        
    #     self.assertEqual(response.status_code, 400)
    