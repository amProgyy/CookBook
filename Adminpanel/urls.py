from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.admin_login, name='admin_login'),
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('users/', views.manage_users, name='manage_users'),
    path('recipes/', views.manage_recipes, name='manage_recipes'),
    path('approve/<int:recipe_id>/', views.approve_recipe, name='admin_approve_recipe'),
    path('reject/<int:recipe_id>/', views.reject_recipe, name='admin_reject_recipe'),
    path('delete-recipe/<int:recipe_id>/', views.delete_recipe, name='admin_delete_recipe'),
    path('delete-user/<int:user_id>/', views.delete_user, name='admin_delete_user'),
    path('add-tag/', views.add_tag, name='admin_add_tag'),
    path('delete-tag/<int:tag_id>/', views.delete_tag, name='admin_delete_tag'),
]