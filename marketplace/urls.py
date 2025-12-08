
from django.urls import path
from . import views

app_name = 'marketplace'
urlpatterns = [
    path('', views.index, name='marketplace_index'),
    path('add-to-cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
]
