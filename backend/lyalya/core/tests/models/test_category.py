from django.test import TestCase
from django.core.exceptions import ValidationError
from ...models import Category

class CategoryModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Создание тестовых данных"""
        
        cls.main_category = Category.objects.create(
            name = 'Main Category',
            slug = 'main-category'
        )

        cls.child_category = Category.objects.create(
            name = 'Child Category',
            slug = 'child-category',
            parent = cls.main_category
        )



    def test_category_creation(self):
        """Тест создания категории"""

        self.assertEqual(self.main_category.name, 'Main Category')
        self.assertEqual(self.main_category.slug, 'main-category')

        self.assertEqual(self.child_category.name, 'Child Category')
        self.assertEqual(self.child_category.slug, 'child-category')
        self.assertEqual(self.child_category.parent, self.main_category)


    def test_optional_parent(self):
        """Тест необязательного поля родительской категории"""

        new_category = Category.objects.create(
            name = 'New Category',
            slug = 'new-category'
        )
        self.assertIsNone(new_category.parent)


    def test_parent_relation(self):
        """Тест связи с родительской категорией"""

        parent = self.child_category._meta.get_field('parent')
        self.assertEqual(parent.remote_field.model, Category)
        self.assertEqual(parent.remote_field.on_delete.__name__, 'SET_NULL')
        self.assertTrue(parent.null)
        self.assertTrue(parent.blank)
        self.assertEqual(parent.remote_field.related_name, 'children')


    def test_str_representation(self):
        """Тест строкового представления"""

        self.assertEqual(str(self.child_category), 'Child Category')


    def test_verbose_name_plural(self):
        """Тест отображения множественного числа"""
        self.assertEqual(Category._meta.verbose_name_plural, 'Categories')
    

    def test_max_len_name(self):
        """Тест максимальной длины названия категории"""

        max_len = self.child_category._meta.get_field('name').max_length
        self.assertEqual(max_len, 255)

    
    def test_max_len_slug(self):
        """Тест максимальной длины slug"""

        max_len = self.child_category._meta.get_field('slug').max_length
        self.assertEqual(max_len, 255)


    def test_unique_slug(self):
        """Тест уникальности slug"""

        with self.assertRaises(ValidationError):

            new_category = Category(
                name='New Category',
                slug='child-category'
            )
            new_category.full_clean()
            new_category.save()