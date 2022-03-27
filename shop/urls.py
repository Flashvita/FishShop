from django.urls import path
from .views import BaseView, CategoriesView, CategoryView, RegistrationCustomerView, LoginView, LogoutUserView
from .views import ProductsView, ProductDetail, CartDetailView, ProductAddToCartView, ProductRemoveFromCartView
from .views import OrderCreateView

urlpatterns = [
    path('cart/cart_detail/', CartDetailView.as_view(), name='cart_detail'),
    path('add/<int:pk>/', ProductAddToCartView.as_view(), name='add_to_cart'),
    path('remove/<int:pk>/', ProductRemoveFromCartView.as_view(), name='remove_from_cart'),
    path('', BaseView.as_view(), name='base'),
    path('catalog/<int:pk>/', CategoriesView.as_view(), name='categories'),
    path('catalog/category_detail/<int:pk>/', CategoryView.as_view(), name='category_detail'),
    path('catalog/products/<int:pk>/', ProductsView.as_view(), name='products'),
    path('registration/customer/', RegistrationCustomerView.as_view(), name='customer'),
    path('registration/login/', LoginView.as_view(), name='login'),
    path('registration/logout/', LogoutUserView.as_view(), name='logout'),
    path('catalog/product_detail/<int:pk>/', ProductDetail.as_view(), name='product_detail'),
    path('orders/order-create/', OrderCreateView.as_view(), name='order-create'),


]
