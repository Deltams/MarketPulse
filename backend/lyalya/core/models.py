from django.conf import settings
from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError


# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.user.username

class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_seller = models.BooleanField(default=False)
    is_buyer = models.BooleanField(default=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


class SellerProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='seller_profile'
    )
    business_name = models.CharField(max_length=255, null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.business_name


class BuyerProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='buyer_profile'
    )


class Brand(models.Model):
    # owner = models.OneToOneField(
    #     UserProfile, on_delete=models.CASCADE, null=True, blank=True
    # )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='brands_owned',
        limit_choices_to={'is_seller': True}
    )
    name = models.CharField(max_length=255, unique=True, null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
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
        Brand,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]) # физически в БД все еще можно записать отрицательную цену!!!

    is_active = models.BooleanField(default=True)
    # seller = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='products')
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='products_offered',
        limit_choices_to={'is_seller': True}
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def check_price(self):
        if self.price < 0:
            raise ValidationError("Цена не может быть отрицательной.")

    def save(self, *args, **kwargs):
        """Переопределяем метод save(), чтобы включить доп. проверку(и)"""
        self.check_price()
        return super().save(*args, **kwargs)


class Service(models.Model):
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='services_offered',
        limit_choices_to={'is_seller': True}
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='services'
    )
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='cart'
    )

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

    def __str__(self):
        if self.user:
            return f"Cart {self.user.email}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)]
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['cart', 'product'],
                name='unique_product_in_cart'
            )
        ]

