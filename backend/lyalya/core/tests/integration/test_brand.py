from rest_framework.test import APITestCase
from rest_framework import status
from ...models import Brand
from ..Bakery import minimal_brand_recipe, full_brand_recipe, user_recipe

class BrandIntegrationTest(APITestCase):
    

    @classmethod
    def setUpTestData(cls):
        """Создание тестовых данных"""

        cls.seller1 = user_recipe.make(username='brand-owner', is_seller=True)

        cls.seller2 = user_recipe.make(username='brand-owner2', is_seller=True)

        cls.random_user = user_recipe.make(username='random_user', is_seller=False)

        cls.first_brand = full_brand_recipe.make(
            name='First Brand',
            slug='first-brand',
            owner=cls.seller1

        )
        
        cls.second_brand = full_brand_recipe.make(
            name='Second Brand',
            slug='second-brand',
            owner=cls.seller2

        )



    # def test_post_brand_by_seller(self):
    #     """Тест POST создания бренда для url api/v1/brandlist/ для продавца"""

    #     self.client.force_authenticate(user=self.seller)

    #     url = 'api/v1/brandlist/'

    #     data = {
    #         'name': 'New Brand',
    #         'slug': 'new-brand',
    #         'is_verified': False
    #     }

    #     response = self.client.post(url, data, format='json')
        
    #     self.assertEqual(response.status_code, 201)
    #     self.assertEqual(response.data['name'], 'New Brand')
    #     self.assertEqual(response.data['slug'], 'new-brand')
    #     self.assertEqual(Brand.objects.count(), 3)


    def test_put_brand_by_seller(self):
        """Тест PUT для api/v1/brandlist/<int:pk>/ для продавца"""
       
        self.client.force_authenticate(user=self.seller1)
    
        url = f'/api/v1/brandlist/{self.first_brand.id}/'

        data = {
            'name': 'Updated Brand',
            'slug': 'updated-brand',
            'owner': self.seller1.id
        }

        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Updated Brand')
        self.assertEqual(response.data['slug'], 'updated-brand')


    def test_put_brand_by_other_seller(self):
        """Тест PUT для api/v1/brandlist/<int:pk>/ для другого продавца"""
       
        self.client.force_authenticate(user=self.seller2)
    
        url = f'/api/v1/brandlist/{self.first_brand.id}/'

        data = {
            'name': 'Updated Brand',
            'slug': 'updated-brand',
            'owner': self.seller2.id
        }

        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, 403)
        self.assertIn('У вас нет прав на редактирование этого бренда', str(response.data))

    def test_put_brand_by_not_seller(self):
        """Тест PUT для api/v1/brandlist/<int:pk>/ для обычного пользователя"""
       
        self.client.force_authenticate(user=self.random_user)
    
        url = f'/api/v1/brandlist/{self.first_brand.id}/'

        data = {
            'name': 'Updated Brand',
            'slug': 'updated-brand',
            'owner': self.seller1.id
        }

        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, 403)



    def test_patch_brand_by_seller(self):
        """Тест PATCH для api/v1/brandlist/<int:pk>/ для продавца"""
       
        self.client.force_authenticate(user=self.seller1)
    
        url = f'/api/v1/brandlist/{self.first_brand.id}/'

        data = {
            'name': 'Updated Brand'
        }

        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Updated Brand')


    def test_patch_brand_by_other_seller(self):
        """Тест PATCH для api/v1/brandlist/<int:pk>/ для другого продавца"""
       
        self.client.force_authenticate(user=self.seller1)
    
        url = f'/api/v1/brandlist/{self.second_brand.id}/'

        data = {
            'name': 'Updated Brand'
        }

        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, 403)


    def test_delete_brand_by_seller(self):
        """Тест DELETE для удаления бренда url api/v1/brandlist/<int:pk>/ для продавца"""

        self.client.force_authenticate(user=self.seller1)

        url = f'/api/v1/brandlist/{self.first_brand.id}/'
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Brand.objects.filter(id=self.first_brand.id).exists()) 


    # def test_delete_brand_by_other_seller(self):
    #     """Тест DELETE для удаления бренда url api/v1/brandlist/<int:pk>/ для другого продавца"""

    #     self.client.force_authenticate(user=self.seller1)

    #     url = f'/api/v1/brandlist/{self.second_brand.id}/'
    #     response = self.client.delete(url)
        
    #     self.assertEqual(response.status_code, 403)
    #     self.assertIn('У вас нет прав на удаление этого бренда', str(response.data))



    