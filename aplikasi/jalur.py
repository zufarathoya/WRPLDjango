from bson import ObjectId
from django.shortcuts import get_object_or_404, render, redirect
from .models import product_collection, user_collection
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
    categories = product_collection.distinct('kategori')

    # Ambil kategori yang dipilih dari permintaan GET
    selected_category = request.GET.get('kategori', '')

    if selected_category:
        products = product_collection.find({'kategori': selected_category})
        products = list(products)
    else:
        products = product_collection.find()
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
        product = product_collection.find_one({'_id': ObjectId(selected_id)})
        product['id'] = product['_id']
        context = {
            'product': product,
            'selected_id': selected_id,
        }
        return render(request, 'pelanggan/buy_product.html', context)
    return render(request, 'pelanggan/buy.html', context)


def toko(request):
    return render(request, 'toko/base.html', {})

def gudang(request):
    user_log = user_collection.find_one({'is_login':True})
    if not user_log or user_log['category'] != 'gudang':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect(reverse('login/'))
    return render(request, 'gudang/base.html', {})

def delivery(request):
    return render(request, 'delivery/base.html', {})

def buy_product(request):
    user_log = user_collection.find_one({'is_login':True})
    if not user_log or user_log['category'] != 'pelanggan':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect(reverse('login/'))
    
    selected_id = request.GET.get('beli', '')
    product = product_collection.find_one({'_id': ObjectId(selected_id)})
    product['id'] = product['_id']
    context = {
        'product': product,
        'selected_id': selected_id,
    }
    return render(request, 'pelanggan/buy_product.html', context)