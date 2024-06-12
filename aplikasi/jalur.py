from bson import ObjectId
from django.shortcuts import get_object_or_404, render, redirect
from .models import product_collection, user_collection
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse

def pelanggan(request):
    return render(request, 'pelanggan/base.html', {})

def buy(request):
        # Ambil semua kategori unik dari koleksi produk
    categories = product_collection.distinct('kategori')

    # Ambil kategori yang dipilih dari permintaan GET
    selected_category = request.GET.get('kategori', '')

    if selected_category:
        products = product_collection.find({'kategori': selected_category})
        # products = list(products)
    else:
        products = product_collection.find()
        # products = list(products)

    # for product in products:
        # product['id'] = product['_id']

    context = {
        'products': products,
        'categories': categories,
        'selected_category': selected_category,
    }
    return render(request, 'pelanggan/buy.html', context)


def toko(request):
    return render(request, 'toko/base.html', {})

def gudang(request):
    return render(request, 'gudang/base.html', {})

def delivery(request):
    return render(request, 'delivery/base.html', {})

def buy_product(request, product_id):
    return HttpResponse(f"You are purchasing product with ID: {product_id}")