from django.test import TestCase 
from rest_framework import status
from django.urls import reverse
from ...models import Brand
from ..Bakery import minimal_brand_recipe


class BrandViewTest(TestCase):
    

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



    def test_all_brands_view(self):
        """Тест представления для url brands/"""

        response = self.client.get('/brands/')
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/brand-list.html')
        self.assertContains(response, 'First Brand')
        self.assertContains(response, 'Second Brand')
        self.assertEqual(set(response.context['brands']), {self.first_brand, self.second_brand})


    def test_brand_by_id_view(self):
        """Тест представления для url brands/<int:pk>/"""

        url = f'/brands/{self.first_brand.id}/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/brand-detail.html')
        self.assertContains(response, 'First Brand')
        self.assertEqual(response.context['brand'], self.first_brand)


    def test_brand_detail_by_invalid_id_view(self):
        """Тест представления для url brands/<int:pk>/ с несуществующим id"""
        
        invalid_id = 99999
        url = f'/brands/{invalid_id}/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
    

    






