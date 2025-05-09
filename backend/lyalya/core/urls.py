from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('cat/', views.cat),

    path('category/<int:cat_id>/', views.category),
    path('category/<slug:cat_slug>/', views.category_by_slug),

    path('api/v1/categorylist/', views.CategoryAPIView.as_view()),
    path('api/v1/categories/', views.CategoryListCreateView.as_view()),
    path('api/v1/categories/<int:pk>/', views.CategoryRetrieveUpdateDestroyView.as_view()),
    
    path('api/v1/productlist/', views.ProductAPIView.as_view()),
    path('api/v1/brandlist/', views.BrandAPIView.as_view()),
    path('api/v1/userprofilelist/', views.UserProfileAPIView.as_view()),
]
