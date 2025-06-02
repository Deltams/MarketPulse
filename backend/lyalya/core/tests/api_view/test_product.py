from rest_framework.test import APITestCase
from rest_framework import status
from ...models import Product
from ..Bakery import minimal_product_recipe

class ProductAPITest(APITestCase):
    

    @classmethod
    def setUpTestData(cls):
        """Создание тестовых данных"""

        cls.first_product = minimal_product_recipe.make(
            name='First Product',
            slug='first-product',
            price=100.00
        )
        
        cls.second_product = minimal_product_recipe.make(
            name='Second Product',
            slug='second-product',
            price=10.00
        )


    def test_get_product_list(self):
        """Тест GET для url /api/v1/productlist/"""

        response = self.client.get('/api/v1/productlist/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['name'], 'First Product')
        self.assertEqual(response.data[1]['name'], 'Second Product')


    def test_get_product_detail(self):
        """Тест GET для url api/v1/productlist/<int:pk>/"""

        url = f'/api/v1/productlist/{self.first_product.id}/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'First Product')

    
    def test_get_product_detail_by_invalid_id(self):
        """Тест для url GET api/v1/productlist/<int:pk>/ с несуществующим id"""

        invalid_id = 99999
        url = f'/api/v1/productlist/{invalid_id}/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)


    def test_put_product_detail(self):
        """Тест PUT для api/v1/productlist/<int:pk>/"""
       
        url = f'/api/v1/productlist/{self.second_product.id}/'

        data = {
            'name': 'Updated Product',
            'slug': 'updated-product',
            'price': 0.99
        }
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Updated Product')
        self.assertEqual(response.data['price'], '0.99')


    def test_patch_product_detail(self):
        """Тест PATCH для url api/v1/productlist/<int:pk>/"""
       
        url = f'/api/v1/productlist/{self.second_product.id}/'

        data = { 'name': 'Patched Product' }
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Patched Product')
        self.assertEqual(response.data['slug'], 'second-product')


    def test_delete_product_detail(self):
        """Тест DELETE для url api/v1/productlist/<int:pk>/"""

        url = f'/api/v1/productlist/{self.second_product.id}/'
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Product.objects.count(), 1)



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
    