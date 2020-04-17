from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='products_index'),
    path('search/', views.search, name='products_search'),
]