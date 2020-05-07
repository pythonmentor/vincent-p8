from django.urls import path
from . import views

# url from /products/
urlpatterns = [
    path('', views.FavouritesView.as_view(), name='products_index'),
    path('search/', views.ProductsView.as_view(), name='products_search'),
    path('category/<category>', views.CompareView.as_view(), name='compare_search'),
    path('<int:pk>', views.ProductDetailView.as_view(), name="product_detail"),
    path('save/<int:pk_health>/<int:pk_unhealth>', views.save, name='product_save')
]