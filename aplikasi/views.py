from bson import ObjectId
from django.shortcuts import render, redirect
from .models import product_collection, user_collection, cart_collection, Product
from django.http import HttpResponse, JsonResponse
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
        products = list(products)

    else:
        products = product_collection.find()
        products = list(products)

    for product in products:
        product["id"] = product["_id"]

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
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        chekUser = user_collection.find_one({'username':username})
        if chekUser:
            messages.error(request, 'Username already exists')
            return render(request, 'autentikasi/register.html', {})
        elif password1 != password2:
            messages.error(request, 'Password not match')
            return render(request, 'autentikasi/register.html', {})
        else:
            user = {
                'email' : email,
                'username': username,
                'password': password1,
                'category': 'pelanggan',
            }
            user_collection.insert_one(user)
            return redirect(reverse('login/'))
        
    return render(request, 'autentikasi/register.html', {})

def buy_product(request):
    if request.method == 'POST':
        selected_product_id = request.POST.get('selected_product_id')
        quantity = int(request.POST.get('quantity', 0))  # Ambil nilai quantity dari formulir, default 0 jika tidak ada
        
        # Pastikan selected_product_id memiliki nilai yang valid
        if not selected_product_id:
            return redirect('product_list')  # Atau arahkan ke halaman lain jika tidak ada selected_product_id
        
        # Ambil produk dari database berdasarkan selected_product_id
        try:
            product = Product.objects.get(id=selected_product_id)
        except Product.DoesNotExist:
            return redirect('product_list')
        
        if quantity <= 0 or quantity > product.stok:
            return redirect('product_list')
        
        # Lakukan logika pembelian produk di sini
        # Misalnya, tambahkan produk ke dalam keranjang belanja atau proses pembayaran
        
        # Setelah pembelian sukses, bisa redirect ke halaman sukses atau halaman lain
        return redirect('success_page')
    
    return redirect('product_list')