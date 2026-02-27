from Recipe import views
from django import urls
from django.urls import path

urlpatterns = [
    path('feed/', views.home_feed, name='home_feed'),
    path('create/', views.create_recipe, name='create_recipe'),
    path('detail/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    path('delete/<int:recipe_id>/', views.delete_ajax, name='delete'),
    path('edit/<int:recipe_id>/', views.edit_recipe, name='edit_recipe'),
    path('nutrition/<int:recipe_id>/', views.nutrition_analysis, name='nutrition_analysis'),
    path('substitute/<str:ingredient_name>/', views.ingredient_substitute, name='ingredient_substitute'),
]
