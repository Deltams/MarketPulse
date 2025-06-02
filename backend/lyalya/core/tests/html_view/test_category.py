from django.test import TestCase 
from rest_framework import status
from django.urls import reverse
from ...models import Category
from ..Bakery import minimal_category_recipe, full_category_recipe


class CategoryViewTest(TestCase):
    

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


    def test_cat_view(self):
        """Тест представления для url cat/"""

        response = self.client.get('/cat/')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), 'categories')


    def test_category_by_id_view(self):
        """Тест представления для url category/<int:cat_id>/"""

        url = f'/category/{self.main_category.id}/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/category.html')
        self.assertContains(response, 'Main Category')
        self.assertEqual(response.context['category'], self.main_category)


# !!!!!!!! Надо ввести статус код 404 для несуществующего id
    # def test_category_by_ivalid_id_view(self):
    #     """Тест представления для url category/<int:cat_id>/ с несуществующим id """

    #     invalid_id = 99999
    #     url = f'/category/{invalid_id}/'
    #     response = self.client.get(url)

    #     self.assertEqual(response.status_code, 404)


    def test_category_by_slug_view(self):
        """Тест представления для url category/<slug:cat_slug>/"""

        url = f'/category/{self.main_category.slug}/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/category.html')
        self.assertContains(response, 'Main Category')
        self.assertEqual(response.context['category'], self.main_category)


    def test_category_by_ivalid_slug_view(self):
        """Тест представления для url category/<slug:cat_slug>/ с несуществующим slug """

        invalid_slug = 'new-category'
        url = f'/category/{invalid_slug}/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)


    def test_all_category_view(self):
        """Тест представления для url categories/"""

        response = self.client.get('/categories/')
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/category-list.html')
        self.assertContains(response, 'Main Category')
        self.assertContains(response, 'Child Category')
        self.assertEqual(set(response.context['categories']), {self.main_category, self.child_category})


    def test_category_detail_by_id_view(self):
        """Тест представления для url categories/<int:pk>"""

        url = f'/categories/{self.main_category.id}/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/category-detail.html')
        self.assertContains(response, 'Main Category')
        self.assertEqual(response.context['category'], self.main_category)


    def test_category_detail_by_invalid_id_view(self):
        """Тест представления для url categories/<int:pk> с несуществующим id"""
        
        invalid_id = 99999
        url = f'/categories/{invalid_id}/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
    

    






