from django.urls import path
from . import views
from . import health

urlpatterns = [
    path("health/", health.health_check),
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('cat/', views.cat),

    path('category/<int:cat_id>/', views.category),
    path('category/<slug:cat_slug>/', views.category_by_slug),

    path('brands/', views.brand_list_view),
    path('brands/<int:pk>/', views.brand_detail_view),
    path('categories/', views.category_list_view),
    path('categories/<int:pk>/', views.category_detail_view),
    path('products/', views.product_list_view),
    path('products/<int:product_id>/', views.product_detail_view),

    path('api/v1/categories/', views.CategoryListCreateView.as_view()),
    path('api/v1/categories/<int:pk>/', views.CategoryRetrieveUpdateDestroyView.as_view()),
    
    path('api/v1/productlist/', views.ProductAPIView.as_view()),
    path('api/v1/productlist/<int:pk>/', views.ProductDetailAPIView.as_view()),

    path('api/v1/servicelist/', views.ServiceAPIView.as_view()),
    path('api/v1/servicelist/<int:pk>/', views.ServiceDetailAPIView.as_view()),

    path('api/v1/brandlist/', views.BrandAPIView.as_view()),
    path('api/v1/brandlist/<int:pk>/', views.BrandDetailAPIView.as_view()),

    path('api/v1/auth/register', views.RegisterView.as_view(), name='register'),
    path('api/v1/auth/user/', views.UserProfileView.as_view(), name='user-profile'),

    path('api/v1/carts/', views.CartListCreateView.as_view()),
    path('api/v1/carts/<int:pk>/',
         views.CartItemRetrieveUpdateDestroyView.as_view()),

    path('api/v1/cart_items/', views.CartItemListCreateView.as_view()),
    path('api/v1/cart_items/<int:pk>/',
         views.CartItemRetrieveUpdateDestroyView.as_view()
         ),

    path('api/v1/address/', views.AddressListCreateView.as_view()),
    path('api/v1/address/<int:pk>/',
         views.AddressRetrieveUpdateDestroyView.as_view()
         ),

    path('api/v1/order/', views.OrderListCreateView.as_view()),
    path('api/v1/order/<int:pk>/',
         views.OrderRetrieveUpdateDestroyView.as_view()
         ),

    path('api/v1/order_items/', views.OrderItemListCreateView.as_view()),
    path('api/v1/order_items/<int:pk>/',
         views.OrderItemRetrieveUpdateDestroyView.as_view()
         ),
]
