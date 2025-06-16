from rest_framework.test import APITestCase
from rest_framework import status
from ..Bakery import full_product_recipe, minimal_brand_recipe, minimal_category_recipe, full_category_recipe, user_recipe
from ...models import Product


class ProductAPITest(APITestCase):
    

    @classmethod
    def setUpTestData(cls):
        """Создание тестовых данных"""

        cls.user1 = user_recipe.make(username='seller1', is_seller=True)
        cls.user2 = user_recipe.make(username='seller2', is_seller=True)
        cls.user3 = user_recipe.make(username='random_user', is_seller=False)

        cls.brand = minimal_brand_recipe.make(
            name='Test Brand',
            slug='test-brand'
        )

        cls.main_category = minimal_category_recipe.make(
            name='Main Category',
            slug='main-category'
        )

        cls.child_category = full_category_recipe.make(
            name='Child Category',
            slug='child-category',
            parent=cls.main_category
        )

        cls.first_product = full_product_recipe.make(
            name='First Product',
            slug='first-product',
            price=100.00,
            category=cls.main_category,
            brand=cls.brand,
            seller=cls.user1
        )
        
        cls.second_product = full_product_recipe.make(
            name='Second Product',
            slug='second-product',
            price=10.00,
            category=cls.child_category,
            brand=None,
            seller=cls.user2
        )



    def test_get_product_list(self):
        """Тест GET для списка продуктов url api/v1/productlist/"""

        url = '/api/v1/productlist/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], 'First Product')
        self.assertEqual(response.data[1]['name'], 'Second Product')


    def test_get_product_detail(self):
        """Тест GET для детальной информации о продукте url api/v1/productlist/<int:pk>/"""

        url = f'/api/v1/productlist/{self.first_product.id}/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'First Product')
        self.assertEqual(response.data['slug'], 'first-product')
        self.assertEqual(response.data['price'], '100.00')


    def test_post_product_list(self):
        """Тест POST для создания продукта url api/v1/productlist/"""

        self.client.force_authenticate(user=self.user1)

        url = '/api/v1/productlist/'
        data = {
            'name': 'New Product',
            'slug': 'new-product',
            'description': 'New Product Description',
            'price': 50.00,
            'category': self.main_category.id,
            'brand': self.brand.id
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], 'New Product')
        self.assertEqual(response.data['slug'], 'new-product')
        self.assertEqual(response.data['price'], '50.00')


    def test_put_product_detail(self):
        """Тест PUT для обновления продукта url api/v1/productlist/<int:pk>/"""

        self.client.force_authenticate(user=self.user1)

        url = f'/api/v1/productlist/{self.first_product.id}/'
        data = {
            'name': 'Updated Product',
            'slug': 'updated-product',
            'description': 'Updated Product Description',
            'price': 199.99,
            'category': self.main_category.id,
            'brand': self.brand.id
        }
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Updated Product')
        self.assertEqual(response.data['slug'], 'updated-product')
        self.assertEqual(response.data['price'], '199.99')


    def test_delete_product_detail(self):
        """Тест DELETE для удаления продукта url api/v1/productlist/<int:pk>/"""

        self.client.force_authenticate(user=self.user1)

        url = f'/api/v1/productlist/{self.first_product.id}/'
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Product.objects.filter(id=self.first_product.id).exists()) 