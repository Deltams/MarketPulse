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

    def test_get_product_detail(self):
        """Тест GET для url api/v1/productlist/<int:pk>/"""

        url = f'/api/v1/productlist/{self.first_product.id}/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'First Product')

    
    def test_get_product_detail_by_non_existent_id(self):
        """Тест для url GET api/v1/productlist/<int:pk>/ с несуществующим id"""

        non_existent_id = 99999
        url = f'/api/v1/productlist/{non_existent_id}/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)


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
    