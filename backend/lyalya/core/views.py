from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from rest_framework import generics

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


class ProductAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()
        
        # Get all category parameters
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
            
            # Apply the filter
            queryset = queryset.filter(category_filters)
            
        return queryset


class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class BrandAPIView(generics.ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class BrandDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class UserProfileAPIView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
