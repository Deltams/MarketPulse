from rest_framework.test import APITestCase
from rest_framework import status
from ..Bakery import full_product_recipe, minimal_brand_recipe, minimal_category_recipe, full_category_recipe


class ProductIntegrationTest(APITestCase):
    

    @classmethod
    def setUpTestData(cls):
        """Создание тестовых данных"""

        cls.brand = minimal_brand_recipe.make(
            name = 'Test Brand',
            slug = 'test-brand'
        )

        cls.main_category = minimal_category_recipe.make(
            name = 'Main Category',
            slug = 'main-category'
        )

        cls.child_category = full_category_recipe.make(
            name = 'Child Category',
            slug = 'child-category',
            parent = cls.main_category
        )

        cls.first_product = full_product_recipe.make(
            name='First Product',
            slug='first-product',
            price=100.00,
            category = cls.main_category,
            brand  = cls.brand
        )
        
        cls.second_product = full_product_recipe.make(
            name='Second Product',
            slug='second-product',
            price=10.00,
            category = cls.child_category,
            brand = None
        )



    def test_product_category(self):
        """Тест отображения продуктом своей категории"""

        product_url = f'/api/v1/productlist/{self.first_product.id}/'
        product_response = self.client.get(product_url)

        self.assertEqual(product_response.status_code, 200)
        category_id = product_response.data['category']

        category_url = f'/api/v1/categories/{category_id}/'
        category_response = self.client.get(category_url)

        self.assertEqual(category_response.status_code, 200) 
        self.assertEqual(category_response.data['name'], 'Main Category')



    def test_product_brand(self):
        """Тест отображения продуктом своего бренда"""

        product_url = f'/api/v1/productlist/{self.first_product.id}/'
        product_response = self.client.get(product_url)

        self.assertEqual(product_response.status_code, 200)
        brand_id = product_response.data['brand']

        brand_url = f'/api/v1/brandlist/{brand_id}/'
        brand_response = self.client.get(brand_url)

        self.assertEqual(brand_response.status_code, 200) 
        self.assertEqual(brand_response.data['name'], 'Test Brand')


    def test_product_without_brand(self):
        """Тест отображения продукта без бренда"""

        url = f'/api/v1/productlist/{self.second_product.id}/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.data.get('brand'))


    def test_product_with_child_category(self):
        """Тест продукта с дочерней категорией"""

        product_url = f'/api/v1/productlist/{self.second_product.id}/'
        product_response = self.client.get(product_url)

        category_id = product_response.data['category']

        category_url = f'/api/v1/categories/{category_id}/'
        category_response = self.client.get(category_url)

        self.assertEqual(category_response.status_code, 200) 
        self.assertEqual(category_response.data['name'], 'Child Category')
        self.assertEqual(category_response.data['parent'], self.main_category.id)



    # def test_filter_products_by_category(self):
    #     """Тест фильтрации продуктов по категории"""

    #     url = f'/api/v1/productlist/?category={self.main_category.id}'
    #     response = self.client.get(url)

    #     self.assertEqual(response.status_code, 200) 
    #     self.assertEqual(len(response.data), 1)
    #     self.assertEqual(response.data[0]['name'], 'First Product')


