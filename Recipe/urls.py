from Recipe import views
from django import urls
from django.urls import path

urlpatterns = [
    path('create_recipe/', views.create_recipe, name='create_recipe'),
]
