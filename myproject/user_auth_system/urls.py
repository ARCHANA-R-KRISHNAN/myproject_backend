from django.urls import path
from . import views

urlpatterns = [
    path('register', views.user_signup,name='user_signup'),
    path('login',views.user_login,name='login'),
    path('profile',views.user_profile,name='profile'),

]
