from rest_framework.test import APITestCase
from rest_framework import status
from ...models import Category
from ...models import Product
from ..Bakery import full_category_recipe, minimal_category_recipe, minimal_product_recipe



class CategoryAPITest(APITestCase):
    

    @classmethod
    def setUpTestData(cls):
        """Создание тестовых данных"""

        cls.main_category = minimal_category_recipe.make(
            name = 'Main Category',
            slug = 'main-category'
        )

        cls.child_category = full_category_recipe.make(
            name = 'Child Category',
            slug = 'child-category',
            parent = cls.main_category
        )



        cls.product1 = minimal_product_recipe.make(
            name = 'Product-1',
            slug = 'product-1',
            category = cls.main_category
        )

        cls.product2 = minimal_product_recipe.make(
            name = 'Product-2',
            slug = 'product-2',
            category = cls.child_category
        )



    def test_get_category_list(self):
        """Тест GET для url /api/v1/categories/"""

        response = self.client.get('/api/v1/categories/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['name'], 'Main Category')
        self.assertEqual(response.data[1]['name'], 'Child Category')


    def test_post_category_list(self):
        """Тест POST для url /api/v1/categories/"""

        url = '/api/v1/categories/'
        
        data = {
            'name': 'New Category',
            'slug': 'new-category'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], 'New Category')
        self.assertEqual(Category.objects.count(), 3)


    def test_get_category_detail(self):
        """Тест для url GET /api/v1/categories/<pk>/"""

        url = f'/api/v1/categories/{self.main_category.id}/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Main Category')

    
    def test_get_category_detail_by_invalid_id(self):
        """Тест для url GET /api/v1/categories/<pk>/ с несуществующим id"""

        invalid_id = 99999
        url = f'/api/v1/categories/{invalid_id}/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)


    def test_put_category_detail(self):
        """Тест PUT для url/api/v1/categories/<pk>/"""
       
        url = f'/api/v1/categories/{self.child_category.id}/'

        data = {
            'name': 'Updated Child',
            'slug': 'updated-child',
            'parent': self.main_category.id
        }
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Updated Child')


    def test_patch_category_detail(self):
        """Тест PATCH для url/api/v1/categories/<pk>/"""
       
        url = f'/api/v1/categories/{self.child_category.id}/'

        data = { 'name': 'Patched Child' }
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Patched Child')
        self.assertEqual(response.data['slug'], 'child-category')


    def test_delete_category_detail(self):
        """Тест DELETE для url /api/v1/categories/<pk>/"""

        url = f'/api/v1/categories/{self.child_category.id}/'
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Category.objects.count(), 1)



    def test_post_category_list_validation(self):
        """Тест валидации для /api/v1/categories/"""

        url = f'/api/v1/categories/'

        data = {
                'name': 'without slug',
                'slug': ''
                }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, 400)



    