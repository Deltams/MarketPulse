from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Brand(models.Model):
    owner = models.OneToOneField(
        UserProfile, on_delete=models.CASCADE, null=True, blank=True
    )
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    parent = models.ForeignKey(
        'self', null=True, blank=True, related_name='children', on_delete=models.SET_NULL)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)


class Cart(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


# class Order(models.Model):
#     user = models.ForeignKey(UserProfile, on_delete=models.SET_NULL)
