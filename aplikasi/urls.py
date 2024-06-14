from django.urls import path
from . import views, jalur, cart, checkout, tambah_stok

urlpatterns = [
    path('', views.index),
    path('add/', views.addProduct),
    path('show/', views.showProduct, name='show/'),
    path('showUser/', views.showUser, name='showUser/'),
    path('login/', views.login_view, name='login/'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout/'),
    path('login_user/', views.login_view, name='login'),
    path('register_user/', views.register_view, name='register/'),
    path('pelanggan/', jalur.pelanggan, name='pelanggan/'),
    path('buy/', jalur.buy, name='buy/'),
    path('toko/', jalur.toko, name='toko/'),
    path('gudang/', jalur.gudang, name='gudang/'),
    path('delivery/', jalur.delivery, name='delivery/'),
    path('buy_product/<str:product_id>/', jalur.buy_product, name='buy_product/'),
    # path('buy_product/', views.buy_product, name='buy_product'),
    path('cart/', cart.add_to_cart, name='cart/'),
    path('show_cart/', cart.cart_view, name='show_cart/'),
    path('hapus_barang', cart.hapus_barang, name='hapus_barang/'),
    path('checkout/', checkout.checkout, name='checkout/'),
    path('order_confirmation/', checkout.orderConfirmation, name='order_confirmation/'),
    path('gudang_show/', tambah_stok.show_product, name='gudang_show/'),
    path('gudang_add_stock/', tambah_stok.addStock, name='gudang_add_stock/'),
    path('tambah_stok/', tambah_stok.show_add_stock, name='tambah_stok/'),
    path('tambah_produk/', tambah_stok.tambah_produk, name='tambah_produk/'),
    path('remove/', cart.hapus_barang, name='remove/')
]
