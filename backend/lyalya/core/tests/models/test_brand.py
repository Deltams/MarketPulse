
# import sys


# path = r"C:\\Users\\kholm\\Desktop\\MarketPulse-main (1)\\MarketPulse-main\\backend\\lyalya\\core"

# sys.path.append(path)
from django.test import TestCase
from django.contrib.auth.models import User
from ...models import UserProfile, Brand, Category

# class BrandModelTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         cls.user = User.objects.create_user(username='testuser', password='12345')
#         cls.user_profile = UserProfile.objects.create(user=cls.user)
#         cls.brand = Brand.objects.create(
#             owner=cls.user_profile,
#             name='Test Brand',
#             slug='test-brand',
#             is_verified=True
#         )

#     def test_brand_creation(self):
#         self.assertEqual(self.brand.name, 'Test Brand')

# print(1)

ans = Category.objects.all()

print(ans)