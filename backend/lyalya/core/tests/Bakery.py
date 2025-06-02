from model_bakery.recipe import Recipe, foreign_key, seq
from django.contrib.auth.models import User
from ..models import UserProfile, Brand, Category, Product, Cart, CartItem




"""Создание пользователя"""
user_recipe = Recipe(
    User,
    username=seq('user'),
    email=seq('user', suffix='@gmail.com'),
    password =seq('password')
)


"""Создание профиля пользователя"""
user_profile_recipe = Recipe(
    UserProfile,
    user=foreign_key(user_recipe)
)


"""Создание бренда(все поля)"""
full_brand_recipe = Recipe(
    Brand,
    name=seq('Test Brand '),
    slug=seq('test-brand-'),
    owner=foreign_key(user_profile_recipe),
    description=seq('Description '),
    is_verified=True
)


"""Создание бренда(только обязательные поля)"""
minimal_brand_recipe = Recipe(
    Brand,
    name=seq('Minimal Brand '),
    slug=seq('minimal-brand-')
)


"""Создание категории(все поля)"""
full_category_recipe = Recipe(
    Category,
    name=seq('Test Category '),
    slug=seq('test-category-'),
    parent=None
)


"""Создание категории(только обязательные поля)"""
minimal_category_recipe = Recipe(
    Category,
    name=seq('Minimal Category '),
    slug=seq('minimal-category-')
)


"""Создание продукта(все поля)"""
full_product_recipe = Recipe(
    Product,
    name=seq('Test Product '),
    slug=seq('test-product-'),
    brand=foreign_key(full_brand_recipe),
    category=foreign_key(full_category_recipe),
    description=seq('Product description '),
    price=100.00,
    is_active=True
)


"""Создание продукта(только обязательные поля)"""
minimal_product_recipe = Recipe(
    Product,
    name=seq('Minimal Product '),
    slug=seq('minimal-product-'),
    price=10.00
)


"""Создание корзины пользователя"""
cart_recipe = Recipe(
    Cart,
    user=foreign_key(user_profile_recipe)
)


"""Создание элемента корзины"""
cart_item_recipe = Recipe(
    CartItem,
    cart=foreign_key(cart_recipe),
    product=foreign_key(full_product_recipe)
)
