from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.exceptions import PermissionDenied

from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from .models import Brand, Category, Product, UserProfile
from .serializers import CategorySerializer, ProductSerializer, BrandSerializer, UserProfileSerializer


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
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductAPIView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get_queryset(self):
        queryset = Product.objects.all()
        
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
        
        return queryset

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user.userprofile)


class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get_queryset(self):
        return Product.objects.all()

    def perform_update(self, serializer):
        # Проверяем, является ли пользователь продавцом этого товара
        if serializer.instance.seller != self.request.user.userprofile:
            raise PermissionDenied("Вы не можете редактировать этот товар")
        serializer.save()

    def perform_destroy(self, instance):
        # Проверяем, является ли пользователь продавцом этого товара
        if instance.seller != self.request.user.userprofile:
            raise PermissionDenied("Вы не можете удалить этот товар")
        instance.delete()


class BrandAPIView(generics.ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class BrandDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class UserProfileAPIView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
