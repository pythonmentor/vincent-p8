from django.urls import path

from . import views

urlpatterns = [
    path('profile/', views.index, name='profile'),
    path('signup/', views.signup, name='signup'),
]