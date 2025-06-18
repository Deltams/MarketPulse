from rest_framework import serializers
from .models import (
    User,
    SellerProfile,
    BuyerProfile,
    Brand, Category, Product, Cart, CartItem)


# class UserProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserProfile
#         fields = '__all__'

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password', 'is_seller', 'is_buyer')

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            is_seller=validated_data.get('is_seller', False),
            is_buyer=validated_data.get('is_buyer', True),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    seller_name = serializers.CharField(source='seller.user.username', read_only=True)
    brand_name = serializers.CharField(source='brand.name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'description', 'price', 'image', 
                 'is_active', 'brand', 'brand_name', 'category', 'category_name',
                 'seller', 'seller_name', 'created_at', 'updated_at']
        read_only_fields = ['seller', 'created_at', 'updated_at']

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Цена не может быть отрицательной")
        return value

    def validate_image(self, value):
        if value:
            # if value.size > 5 * 1024 * 1024:  # 5MB
            #     raise serializers.ValidationError("Размер изображения не может превышать 5MB")
            if not value.content_type.startswith('image/'):
                raise serializers.ValidationError("Файл должен быть изображением")
        return value

class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'is_seller', 'is_buyer', 'role')
        read_only_fields = ('id', 'email', 'is_seller', 'is_buyer', 'role')

    def get_role(self, obj):
        if obj.is_seller:
            return 'seller'
        elif obj.is_buyer:
            return 'buyer'
        return 'buyer'  # default role

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'
