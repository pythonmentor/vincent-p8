from django.urls import path

from . import views

app_name = 'account'
urlpatterns = [
    path('profile/', views.index, name='profile'),
    path('signup/', views.signup, name='signup'),
]
