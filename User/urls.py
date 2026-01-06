from django.urls import path
from User import views

urlpatterns = [
    path('signup/', views.user_signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('my_cookbook', views.my_cookbooks, name='my_cookbooks'),
]
