from django.shortcuts import render, redirect
from .models import product_collection, user_collection
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse

# Create your views here.

def index(request):
    return HttpResponse('<h1> Running..... </h1>')

def addProduct(request):
    record = {
        'nama' : 'Nggak tahu',
        'harga' : 10000,
        'stok' : 10,
        'kategori' : 'Skincare' 
    }
    product_collection.insert_one(record)
    return HttpResponse('<h1> Product Added </h1>') 

def showProduct(request):
    # Ambil semua kategori unik dari koleksi produk
    categories = product_collection.distinct('kategori')
    categories = dict(categories)

    # Ambil kategori yang dipilih dari permintaan GET
    selected_category = request.GET.get('kategori', '')

    if selected_category:
        products = product_collection.find({'kategori': selected_category})
    else:
        products = product_collection.find()

    context = {
        'products': products,
        'categories': categories,
        'selected_category': selected_category,
    }
    return render(request, 'main/show_product.html', context)

def showUser(request):
    product = user_collection.find()
    # return HttpResponse(product)
    product_list = list(product)
    return render(request, 'main/user.html', {'products': product_list})


# def login_view(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request, request.POST)
#         if form.is_valid():
#             login(request, form.get_user())
#             return redirect('main/show_product.html')
#     else:
#         form = AuthenticationForm()
#     return render(request, 'autentikasi/login.html', {'form': form})

# def findUser(request):
#     user = user_collection.find()
#     user_list = list(user)
#     return render(request, 'main/show_user.html', {'users': user_list})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = user_collection.find_one({'username':username, 'password':password})
        user = dict(user)
        print(user)
        if len(user):
            if user['category'] == 'pelanggan':
            # return redirect(reverse('show/'))
                return redirect(reverse('pelanggan/'))
            elif user['category'] == 'gudang':
                return redirect(reverse('gudang/'))
            elif user['category'] == 'toko':
                return redirect(reverse('toko/'))
            elif user['category'] == 'delivery':
                return redirect(reverse('delivery/'))
        else:
            messages.error(request, 'Username or password is incorrect')
            return render(request, 'autentikasi/login.html', {})
    else:
        return render(request, 'autentikasi/login.html', {})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'autentikasi/register.html', {'form': form})
