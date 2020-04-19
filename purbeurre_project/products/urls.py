from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='products_index'),
    path('search/', views.ProductsView.as_view(), name='products_search'),
]