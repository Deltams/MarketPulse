from django.contrib import admin
from .models import (
    User,
    SellerProfile,
    BuyerProfile,
    Brand, Category, Product, Service, Cart, CartItem,
    Address, Order, OrderItem
)


admin.site.register(User)
# admin.site.register(SellerProfile)
# admin.site.register(BuyerProfile)
admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Service)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Address)
admin.site.register(Order)
admin.site.register(OrderItem)
