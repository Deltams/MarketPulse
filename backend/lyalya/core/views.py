from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.exceptions import PermissionDenied

from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .models import Brand, Category, Product, Service, Cart, CartItem, Address, Order, OrderItem
from .serializers import (
    CategorySerializer, RegisterSerializer, ProductSerializer, BrandSerializer, UserSerializer,
    ServiceSerializer, CartSerializer, CartItemSerializer, AddressSerializer, OrderSerializer, OrderItemSerializer,
    CustomTokenObtainPairSerializer
)
from .pagination import CustomPageNumberPagination
from rest_framework_simplejwt.views import TokenObtainPairView

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Можно сразу выдать токен, если нужно
            return Response({'user': RegisterSerializer(user).data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def index(request):
    data = {'title': 'Главная страница'}
    return render(request, 'core/index.html', data)


def about(request):
    data = {'title': 'О нас'}
    return render(request, 'core/about.html', data)


def cat(request):
    return HttpResponse('categories')


def category(request, cat_id):
    c = Category.objects.filter(pk=cat_id)[0]
    # c = get_object_or_404(Category, pk=cat_id)
    data = {'category': c}
    return render(request, 'core/category.html', data)


def category_by_slug(request, cat_slug):
    c = get_object_or_404(Category, slug=cat_slug)
    data = {'category': c}
    return render(request, 'core/category.html', data)


def brand_list_view(request):
    brands = Brand.objects.all()
    return render(request, 'core/brand-list.html', {'brands': brands})


def brand_detail_view(request, pk):
    brand = get_object_or_404(Brand, pk=pk)
    return render(request, 'core/brand-detail.html', {'brand': brand})


def category_list_view(request):
    categories = Category.objects.all()
    return render(request, 'core/category-list.html', {'categories': categories})


def category_detail_view(request, pk):
    category = get_object_or_404(Category, pk=pk)
    return render(request, 'core/category-detail.html', {'category': category})


def product_list_view(request):
    products = Product.objects.all()
    return render(request, 'core/product-list.html', {'products': products})


def product_detail_view(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'core/product-detail.html', {'product': product})



class CategoryListCreateView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        # Возвращаем только категории, в которых есть продукты
        return Category.objects.filter(product__isnull=False).distinct()


class ServiceCategoryListCreateView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        # Возвращаем только категории, в которых есть услуги
        return Category.objects.filter(services__isnull=False).distinct()


class CategoryAllListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductAPIView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        queryset = Product.objects.all()
        
        # Фильтрация по бренду
        brand_id = self.request.query_params.get('brand')
        if brand_id:
            queryset = queryset.filter(brand_id=brand_id)
        
        # Фильтрация по категориям
        category_params = {k: v for k, v in self.request.query_params.items() if k.startswith('category_')}
        if category_params:
            from django.db.models import Q
            category_filters = Q()
            for category_id in category_params.values():
                try:
                    category_id = int(category_id)
                    category_filters |= Q(category_id=category_id)
                except (ValueError, TypeError):
                    continue
            queryset = queryset.filter(category_filters)
        
        # Фильтрация по цене
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        # Поиск по названию
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(name__icontains=search)
        
        return queryset.order_by('-created_at', 'id')

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user.userprofile)


class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get_queryset(self):
        return Product.objects.all()
    
    def check_seller_permission(self, product):
        return product.seller == self.request.user
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if not self.check_seller_permission(instance):
            return Response(
                {"detail": "У вас нет прав на редактирование этого товара"},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)

    def perform_update(self, serializer):
        if serializer.instance.seller != self.request.user:
            raise PermissionDenied("Вы не можете редактировать этот товар")
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if not self.check_seller_permission(instance):
            return Response(
                {"detail": "У вас нет прав на удаление этого товара"},
                status=status.HTTP_403_FORBIDDEN
            )
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class BrandAPIView(generics.ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class BrandDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

    def get_permissions(self):
        if self.request.method in ['GET']:
            return []
        return [IsAuthenticated()]
    
    def check_owner_permission(self, brand):
        return brand.owner == self.request.user
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if not self.check_owner_permission(instance):
            return Response(
                {"detail": "У вас нет прав на редактирование этого бренда"},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)

    def perform_update(self, serializer):
        # Проверяем, является ли пользователь владельцем этого бренда
        if serializer.instance.owner != self.request.user:
            raise PermissionDenied("Вы не можете редактировать этот бренд")
        serializer.save()

    def perform_destroy(self, instance):
        if not self.check_owner_permission(instance):
            return Response(
                {"detail": "У вас нет прав на удаление этого бренда"},
                status=status.HTTP_403_FORBIDDEN
            )
        instance.delete()


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class CartListCreateView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class CartRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class CartItemListCreateView(generics.ListCreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer


class CartItemRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer


class AddressListCreateView(generics.ListCreateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer


class AddressRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer


class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderItemListCreateView(generics.ListCreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


class OrderItemRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


class ServiceAPIView(generics.ListCreateAPIView):
    serializer_class = ServiceSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        queryset = Service.objects.all()
        
        # Фильтрация по бренду (теперь напрямую)
        brand_id = self.request.query_params.get('brand')
        if brand_id:
            queryset = queryset.filter(brand_id=brand_id)
        
        # Фильтрация по категориям
        category_params = {k: v for k, v in self.request.query_params.items() if k.startswith('category_')}
        if category_params:
            from django.db.models import Q
            category_filters = Q()
            for category_id in category_params.values():
                try:
                    category_id = int(category_id)
                    category_filters |= Q(category_id=category_id)
                except (ValueError, TypeError):
                    continue
            queryset = queryset.filter(category_filters)
        
        # Фильтрация по цене
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        # Поиск по названию
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(name__icontains=search)
        
        return queryset.order_by('-created_at', 'id')

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)


class ServiceDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def perform_update(self, serializer):
        serializer.save(seller=self.request.user)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
