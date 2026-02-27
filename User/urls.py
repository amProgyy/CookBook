from django.urls import path
from User import views

urlpatterns = [
    path('signup/', views.user_signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('my_cookbook/', views.my_cookbooks, name='my_cookbooks'),
    path('favorites/', views.favorite_recipes, name='favorite_recipes'),
    path('toggle-favorite/<int:recipe_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
    path('notifications/', views.notifications_view, name='notifications'),
]
