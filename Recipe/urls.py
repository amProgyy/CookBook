from Recipe import views
from django import urls
from django.urls import path

urlpatterns = [
    path('create/', views.create_recipe, name='create_recipe'),
    path('detail/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    path("recipe/scale/<int:recipe_id>", views.scale_ingredients, name="scale_ingredients"),

]
