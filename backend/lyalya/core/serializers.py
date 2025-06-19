from rest_framework import serializers
from .models import (
    User,
    SellerProfile,
    BuyerProfile,
    Brand, Category, Product, Service, Cart, CartItem,
    Address, Order, OrderItem
)
from django.db.utils import IntegrityError
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


# class UserProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserProfile
#         fields = '__all__'

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="Пользователь с таким email уже существует."
            )
        ]
    )
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password', 'is_seller', 'is_buyer')

    def create(self, validated_data):
        try:
            user = User(
                email=validated_data['email'],
                username=validated_data['username'],
                is_seller=validated_data.get('is_seller', False),
                is_buyer=validated_data.get('is_buyer', True),
            )
            user.set_password(validated_data['password'])
            user.save()
            # Создаем профиль покупателя/продавца
            if user.is_buyer:
                BuyerProfile.objects.create(user=user)
            if user.is_seller:
                SellerProfile.objects.create(user=user)
            return user
        except IntegrityError:
            raise serializers.ValidationError({'email': ['Пользователь с таким email уже существует.']})
        except Exception as e:
            raise e

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Пользователь с таким email уже существует.")
        return value


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    seller_name = serializers.CharField(source='seller.username', read_only=True)
    brand_name = serializers.CharField(source='brand.name', read_only=True)
    brand_is_verified = serializers.BooleanField(source='brand.is_verified', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'description', 'price', 'image', 
                 'is_active', 'brand', 'brand_name', 'brand_is_verified', 'category', 'category_name',
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


class ServiceSerializer(serializers.ModelSerializer):
    seller_name = serializers.CharField(source='seller.username', read_only=True)
    brand_name = serializers.CharField(source='brand.name', read_only=True)
    brand_is_verified = serializers.BooleanField(source='brand.is_verified', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Service
        fields = ['id', 'name', 'slug', 'description', 'price', 
                 'is_active', 'brand', 'brand_name', 'brand_is_verified', 'category', 'category_name',
                 'seller', 'seller_name', 'created_at', 'updated_at']
        read_only_fields = ['seller', 'created_at', 'updated_at']

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Цена не может быть отрицательной")
        return value


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    service_name = serializers.CharField(source='service.name', read_only=True)
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)
    service_price = serializers.DecimalField(source='service.price', max_digits=10, decimal_places=2, read_only=True)
    product_image = serializers.CharField(source='product.image', read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'item_type', 'product', 'service', 'quantity', 
                 'product_name', 'service_name', 'product_price', 'service_price', 'product_image']

    def validate(self, data):
        item_type = data.get('item_type', 'product')
        product = data.get('product')
        service = data.get('service')

        if item_type == 'product' and not product:
            raise serializers.ValidationError("Для товара должно быть указано поле product")
        elif item_type == 'service' and not service:
            raise serializers.ValidationError("Для услуги должно быть указано поле service")
        
        if product and service:
            raise serializers.ValidationError("Нельзя указывать одновременно товар и услугу")

        return data


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'
