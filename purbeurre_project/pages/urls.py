from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'pages'
urlpatterns = [
    path('', views.index, name='index'),
    path('mentions-legales/', views.legals, name='legals'),
]