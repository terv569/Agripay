from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='home'),
    path('users/', views.users_list, name='users'),
    path('farmers/', views.farmers_list, name='farmers'),
    path('products/', views.products_list, name='products'),
    path('payments/', views.payments_list, name='payments'),
]
