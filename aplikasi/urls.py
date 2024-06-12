from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('add/', views.addProduct),
    path('show/', views.showProduct, name='show/'),
    path('showUser/', views.showUser, name='showUser/'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('login_user/', views.login_view, name='login'),
    path('register_user/', views.register_view, name='register'),
]
