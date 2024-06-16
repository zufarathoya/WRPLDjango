from bson import ObjectId
from django.shortcuts import get_object_or_404, render, redirect
from .models import product_collection, user_collection, sales_product, history_purchase, delivery_req
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse

def pelanggan(request):
    user_log = user_collection.find_one({'is_login':True})
    if not user_log or user_log['category'] != 'pelanggan':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect(reverse('login/'))
    
    return redirect(reverse('buy/'))

def buy(request):
    user_log = user_collection.find_one({'is_login':True})
    if not user_log or user_log['category'] != 'pelanggan':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect(reverse('login/'))

    # Ambil semua kategori unik dari koleksi produk
    categories = sales_product.distinct('kategori')

    # Ambil kategori yang dipilih dari permintaan GET
    selected_category = request.GET.get('kategori', '')

    if selected_category:
        products = sales_product.find({'kategori': selected_category})
        products = list(products)
    else:
        products = sales_product.find()
        products = list(products)

    for product in products:
        product['id'] = product['_id']

    context = {
        'products': products,
        'categories': categories,
        'selected_category': selected_category,
    }
    selected_id = request.GET.get('beli', '')
    if selected_id:
        product = sales_product.find_one({'_id': ObjectId(selected_id)})
        product['id'] = product['_id']
        context = {
            'product': product,
            'selected_id': selected_id,
        }
        return render(request, 'pelanggan/buy_product.html', context)
    return render(request, 'pelanggan/buy.html', context)


def toko(request):
    user_log = user_collection.find_one({'is_login':True})
    if not user_log or user_log['category'] != 'toko':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect(reverse('login/'))
    return render(request, 'toko/base.html', {})

def gudang(request):
    user_log = user_collection.find_one({'is_login':True})
    if not user_log or user_log['category'] != 'gudang':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect(reverse('login/'))
    return render(request, 'gudang/base.html', {})

def delivery(request):
    user_log = user_collection.find_one({'is_login':True})
    if not user_log or user_log['category'] != 'delivery':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect(reverse('login/'))
    return render(request, 'delivery/base.html', {})

def buy_product(request):
    user_log = user_collection.find_one({'is_login':True})
    if not user_log or user_log['category'] != 'pelanggan':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect(reverse('login/'))
    
    selected_id = request.GET.get('beli', '')
    product = sales_product.find_one({'_id': ObjectId(selected_id)})
    product['id'] = product['_id']
    context = {
        'product': product,
        'selected_id': selected_id,
    }
    return render(request, 'pelanggan/buy_product.html', context)

def buyer_history(request):
    user_log = user_collection.find_one({'is_login':True})
    if not user_log or user_log['category'] != 'pelanggan':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect(reverse('login/'))
    
    daftar = history_purchase.find({'user_id': str(user_log['_id'])})
    daftar = list(daftar)
    
    for item in daftar:
        item['total'] = item['total_price'] + item['ongkir']
        
    context = {
        'daftar': daftar,
        # 'total_harga_keranjang': total_harga_keranjang
    }
    
    return render(request, 'pelanggan/history_pesanan.html', context)

def location(request):
    user_log = user_collection.find_one({'is_login':True})
    if not user_log or user_log['category'] != 'pelanggan':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect(reverse('login/'))
    
    total_harga = request.POST.get('total_harga')
    context = {
        'total_harga': total_harga
    }
    return render(request, 'pelanggan/lokasi_pengiriman.html', {})

def status_pengiriman(request):
    user_log = user_collection.find_one({'is_login':True})
    if not user_log or user_log['category'] != 'pelanggan':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect(reverse('login/'))
    
    req = delivery_req.find({'user_id':str(user_log['_id'])})
    req = list(req)
    
    req.sort(key=lambda r: r['date'], reverse=True)

    context = {
        'requests': req
    }

    return render(request, 'pelanggan/status_pengiriman.html', context)