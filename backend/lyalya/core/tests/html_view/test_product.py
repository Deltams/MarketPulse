from django.test import TestCase 
from rest_framework import status
from django.urls import reverse
from ...models import Product
from ..Bakery import minimal_product_recipe

class ProductViewTest(TestCase):
    

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



    def test_all_products_view(self):
        """Тест представления для url products/"""

        response = self.client.get('/products/')
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/product-list.html')
        self.assertContains(response, 'First Product')
        self.assertContains(response, 'Second Product')
        self.assertEqual(set(response.context['products']), {self.first_product, self.second_product})


    def test_product_detail_by_id_view(self):
        """Тест представления для url products/<int:product_id>/"""

        url = f'/products/{self.first_product.id}/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/product-detail.html')
        self.assertContains(response, 'First Product')
        self.assertEqual(response.context['product'], self.first_product)


    def test_product_detail_by_non_existent_id_view(self):
        """Тест представления для url products/<int:product_id> с несуществующим id"""
        
        non_existent_id = 99999
        url = f'/products/{non_existent_id}/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
    

    






