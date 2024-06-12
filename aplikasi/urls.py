from django.urls import path
from . import views, jalur

urlpatterns = [
    path('', views.index),
    path('add/', views.addProduct),
    path('show/', views.showProduct, name='show/'),
    path('showUser/', views.showUser, name='showUser/'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('login_user/', views.login_view, name='login'),
    path('register_user/', views.register_view, name='register/'),
    path('pelanggan/', jalur.pelanggan, name='pelanggan/'),
    path('buy/', jalur.buy, name='buy/'),
    path('toko/', jalur.toko, name='toko/'),
    path('gudang/', jalur.gudang, name='gudang/'),
    path('delivery/', jalur.delivery, name='delivery/'),
    path('buy_product/<int:product_id>/', jalur.buy_product, name='buy-product'),
]
