from django.test import TestCase 
from rest_framework import status
from django.urls import reverse



class MainViewTest(TestCase):
    

    def test_index_view(self):
        """Тест главной страницы"""

        response = self.client.get(reverse('index'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/index.html')
        self.assertEqual(response.context['title'], 'Главная страница')


    def test_about_view(self):
        """Тест страницы о нас'"""

        response = self.client.get(reverse('about'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/about.html')
        self.assertEqual(response.context['title'], 'О нас')
        


    






