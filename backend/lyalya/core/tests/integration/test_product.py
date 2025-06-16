from rest_framework.test import APITestCase
from rest_framework import status
from ..Bakery import full_product_recipe, minimal_brand_recipe, minimal_category_recipe, full_category_recipe, user_recipe


class ProductIntegrationTest(APITestCase):
    

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


    def test_filter_products_by_category(self):
        """Тест фильтрации продуктов по 1 категории"""

        url = f'/api/v1/productlist/?category_1={self.main_category.id}'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200) 
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'First Product')
        self.assertEqual(response.data[0]['category'], self.main_category.id)


    def test_filter_products_by_2_categories(self):
        """Тест фильтрации продуктов по 2 категориям"""

        url = f'/api/v1/productlist/?category_1={self.main_category.id}&category_2={self.child_category.id}'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200) 
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], 'First Product')
        self.assertEqual(response.data[0]['category'], self.main_category.id)
        
        self.assertEqual(response.data[1]['name'], 'Second Product')
        self.assertEqual(response.data[1]['category'], self.child_category.id)


    def test_filter_products_by_non_existent_categories(self):
        """Тест фильтрации продуктов по несуществующей категории"""

        invalid_id = 9999

        url = f'/api/v1/productlist/?category_1={invalid_id}'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200) 
        self.assertEqual(len(response.data), 0)


    def test_filter_products_by_invalid_categories(self):
        """Тест фильтрации продуктов по некорректной категории"""

        url = f'/api/v1/productlist/?category_1=Main_Category'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200) 
        self.assertEqual(len(response.data), 2)


    def test_put_product_by_seller(self):
        """Тест PUT для авторизованного продавца api/v1/productlist/<int:pk>/"""

        self.client.force_authenticate(user=self.user1)

        url = f'/api/v1/productlist/{self.first_product.id}/'

        data = {
            'name': 'Updated Product',
            'slug': 'updated-product',
            'price': 199.99,
        }

        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Updated Product')
        self.assertEqual(response.data['price'], '199.99')


    def test_validate_negative_price(self):
        """Тест PUT с отрицательной ценой api/v1/productlist/<int:pk>/"""

        self.client.force_authenticate(user=self.user1)

        url = f'/api/v1/productlist/{self.first_product.id}/'

        data = {
            'name': 'Updated Product',
            'slug': 'updated-product',
            'price': -100.00,
        }

        response = self.client.put(url, data, format='json')
    
        self.assertEqual(response.status_code, 400)
        self.assertIn('Ensure this value is greater than or equal to 0', str(response.data))


    def test_delete_product_by_seller(self):
        """Тест DELETE для авторизованного продавца url api/v1/productlist/<int:pk>/"""

        self.client.force_authenticate(user=self.user2)

        url = f'/api/v1/productlist/{self.second_product.id}/'
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, 204)


    def test_delete_product_by_non_seller(self):
        """Тест DELETE для НЕ продовца товара url api/v1/productlist/<int:pk>/"""

        self.client.force_authenticate(user=self.user3)

        url = f'/api/v1/productlist/{self.second_product.id}/'
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, 403)



        



    # def test_put_product_by_random_user(self):
    #     """Тест PUT для любого авторизованного пользователя api/v1/productlist/<int:pk>/"""

    #     self.client.force_authenticate(self.random_user)

    #     url = f'/api/v1/productlist/{self.first_product.id}/'

    #     data = {
    #         'name': 'Updated Product',
    #         'slug': 'updated-product',
    #         'price': 199.99,
    #     }

    #     response = self.client.put(url, data, format='json')

    #     self.assertEqual(response.status_code, 403)


    #  def test_patch_product_detail(self):
    #     """Тест PATCH для url api/v1/productlist/<int:pk>/"""
       
    #     url = f'/api/v1/productlist/{self.second_product.id}/'

    #     data = { 'name': 'Patched Product' }
    #     response = self.client.patch(url, data, format='json')
        
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.data['name'], 'Patched Product')
    #     self.assertEqual(response.data['slug'], 'second-product')







