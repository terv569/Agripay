
from django.urls import path
from . import views

app_name = 'farmers'
urlpatterns = [
    path('', views.index, name='farmers_index'),
    path('<int:pk>/', views.profile, name='farmer_profile'),
    path('product/create/', views.create_product, name='create_product'),
    path('product/<int:pk>/edit/', views.edit_product, name='edit_product'),
    path('product/<int:pk>/delete/', views.delete_product, name='delete_product'),
]
