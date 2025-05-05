
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from rest_framework import generics

from .models import Brand, Category, Product
from .serializers import CategorySerializer, ProductSerializer

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


class CategoryAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer