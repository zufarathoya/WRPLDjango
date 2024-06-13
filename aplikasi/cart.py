from bson import ObjectId
from django.shortcuts import render, redirect
from .models import product_collection, user_collection, cart_collection
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse

def cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('selected_product_id')
        username = request.POST.get('username123')
        quantity = int(request.POST.get('quantity'))  # Ensure quantity is an integer
        
        # Mencari produk berdasarkan ID
        product = product_collection.find_one({'_id': ObjectId(product_id)})
        
        # Mencari user berdasarkan username
        user = user_collection.find_one({'username': username})
        
        if product and user:
            # Ubah _id produk menjadi string untuk keperluan render template
            product['id'] = str(product['_id'])
            
            # Hitung harga total untuk produk tertentu
            total_harga_produk = int(product['harga']) * quantity
            
            coba = cart_collection.find_one({'product_id': ObjectId(product_id)})
            if coba is None:
                # Simpan data produk ke dalam koleksi cart_collection
                cart_collection.insert_one({
                    'product_id': str(product_id),
                    'nama': product['nama'],
                    'harga': product['harga'],
                    'kuantitas': quantity,
                    'kategori': product['kategori'],
                    'user_id': str(user['_id']),  # Simpan user_id sebagai string
                    'total_harga_produk': total_harga_produk  # Menyimpan total harga produk
                })
            else:
                # Pastikan 'kuantitas' dalam database adalah tipe numerik (integer)
                current_quantity = int(coba['kuantitas'])
                new_quantity = current_quantity + quantity
                new_total_harga = coba['total_harga_produk'] + total_harga_produk
                
                cart_collection.update_one({'product_id': str(product_id)}, {
                    '$set': {'kuantitas': new_quantity, 'total_harga_produk': new_total_harga}
                })
                
            # Ambil daftar produk dari keranjang untuk user yang sedang login
            daftar = cart_collection.find({'user_id': str(user['_id'])})
            daftar = list(daftar)
            
            # Menghitung total harga semua produk dalam keranjang
            total_harga_keranjang = 0
            for item in daftar:
                total_harga_keranjang += item['total_harga_produk']

            
            context = {
                'product': product,
                'user_id': str(user['_id']),
                'daftar': daftar,
                'total_harga_keranjang': total_harga_keranjang  # Menambahkan total harga keranjang ke dalam konteks
            }
            
            # Render halaman cart.html dengan konteks yang telah dibuat
            return render(request, 'pelanggan/cart.html', context)
        else:
            # Tampilkan pesan error jika produk atau user tidak ditemukan
            return HttpResponse('Error: Product or user not found.')
    
    # Tampilkan pesan error jika metode request tidak valid (bukan POST)
    return HttpResponse('Error: Invalid request method.')

def hapus_barang(request):
    if request.method == 'POST':
        product_id = request.POST.get('selected_product_id')
        user_id = request.POST.get('selected_user_id')
        
        # Hapus barang dari keranjang berdasarkan product_id dan user_id
        cart_collection.delete_one({'product_id': ObjectId(product_id), 'user_id': user_id})

    # Tampilkan pesan error jika metode request tidak valid (bukan POST)
    return HttpResponse('Error: Invalid request method.')

# def cart_view(request):
#     return redirect(reverse('pelanggan/cart.html'))