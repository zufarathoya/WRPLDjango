from bson import ObjectId
from django.shortcuts import render, redirect
from .models import product_collection, user_collection, cart_collection, sales_product
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse

def add_to_cart(request):
    user_log = user_collection.find_one({'is_login':True})
    if not user_log or user_log['category'] != 'pelanggan':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect(reverse('login/'))

    if request.method == 'POST':
        product_id = request.POST.get('selected_product_id')
        username = request.POST.get('username123')
        quantity = int(request.POST.get('quantity'))  # Ensure quantity is an integer
        
        # Mencari produk berdasarkan ID
        product = sales_product.find_one({'_id': ObjectId(product_id)})
        
        # kuantitas tidak lebih dari stok barang
        if quantity > product['stok']:
            messages.error(request, 'Quantity exceeds stock.')
            return redirect(reverse('buy/'))

        user = user_log

        # user = user_collection.find_one({'username': username})
        # user = user_collection.find_one({'is_login': True})
        
        if product and user:
            product['id'] = str(product['_id'])

            total_harga_produk = int(product['harga']) * quantity
            
            coba = cart_collection.find_one({'product_id': str(product_id)})
            if coba is None:
                cart_collection.insert_one({
                    'product_id': product_id,
                    'nama': product['nama'],
                    'harga': product['harga'],
                    'kuantitas': quantity,
                    'kategori': product['kategori'],
                    'user_id': str(user['_id']),  
                    'total_harga_produk': total_harga_produk  
                })
            else:
                current_quantity = int(coba['kuantitas'])
                new_quantity = current_quantity + quantity
                new_total_harga = coba['total_harga_produk'] + total_harga_produk

                if new_quantity > product['stok']:
                    messages.error(request, 'Quantity exceeds stock.')
                    return redirect(reverse('buy/'))
                
                cart_collection.update_one({'product_id': str(product_id)}, {
                    '$set': {'kuantitas': new_quantity, 'total_harga_produk': new_total_harga}
                })

            daftar = cart_collection.find({'user_id': str(user['_id'])})
            daftar = list(daftar)
            
            total_harga_keranjang = 0
            for item in daftar:
                total_harga_keranjang += item['total_harga_produk']

            added = True
            if added:
                message = 'Product is added to cart'
            context = {
                'product': product,
                'user_id': str(user['_id']),
                'daftar': daftar,
                'total_harga_keranjang': total_harga_keranjang,
                'message': message,
            }
            
            # Render halaman cart.html dengan konteks yang telah dibuat
            return render(request, 'pelanggan/buy_product.html', context)
            
        else:
            # Tampilkan pesan error jika produk atau user tidak ditemukan
            return HttpResponse('Error: Product or user not found.')
    
    # Tampilkan pesan error jika metode request tidak valid (bukan POST)
    return HttpResponse('Error: Invalid request method.')

def hapus_barang(request):
    user_log = user_collection.find_one({'is_login':True})
    if not user_log or user_log['category'] != 'pelanggan':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect(reverse('login/'))
    
    if request.method == 'POST':
        product_id = request.POST.get('selected_product_id')
        user_id = request.POST.get('selected_user_id')
        # product_id = request.POST.get('selected_product_id')
        # user_id = user_collection.find_one({'is_login':True})
        
        # Hapus barang dari keranjang berdasarkan product_id dan user_id
        cart_collection.delete_one({'product_id': str(product_id), 'user_id': str(user_id)})
        
        print(f"Product ID: {product_id}")
        print(f"User ID: {user_id}")

        return redirect(reverse('show_cart/'))
        
    # Tampilkan pesan error jika metode request tidak valid (bukan POST)
    # return HttpResponse('Error: Invalid request method.')

def cart_view(request):
    user_log = user_collection.find_one({'is_login':True})
    if not user_log or user_log['category'] != 'pelanggan':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect(reverse('login/'))
    
    # Ambil user yang sedang login
    user = user_collection.find_one({'is_login': True})

    # Ambil daftar produk dari keranjang untuk user yang sedang login
    daftar = cart_collection.find({'user_id': str(user['_id'])})
    daftar = list(daftar)

    total_harga_keranjang = 0

    for item in daftar:
        total_harga_keranjang += item['total_harga_produk']

    content = {
        'daftar': daftar,
        'user_id': str(user['_id']),
        'total_harga_keranjang': total_harga_keranjang,
    }


    return render(request, 'pelanggan/cart.html', content)