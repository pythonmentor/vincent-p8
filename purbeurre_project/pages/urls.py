from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('mentions-legales/', views.legals, name='legals'),
]