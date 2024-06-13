from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from .models import cart_collection, product_collection, history_purchase
from bson import ObjectId
from datetime import datetime

def checkout(request):
    if request.method == 'POST':
        # Ambil data yang dikirim dari form
        selected_user_id = request.POST.get('_user_id')
        total_price = request.POST.get('total_harga')
        
        # Ambil semua item dari keranjang untuk user yang sedang login
        cart_items = cart_collection.find({'user_id': str(selected_user_id)})
        cart_items = list(cart_items)
        # Kurangi kuantitas produk di product_collection
        for item in cart_items:
            product_id = item['product_id']
            cart_quantity = item['kuantitas']
            
            # Cari produk di product_collection
            product = product_collection.find_one({'_id': product_id})
            if product:
                # Kurangi kuantitas produk
                new_quantity = int(product['kuantitas']) - cart_quantity
                product_collection.update_one({'_id': product_id}, {'$set': {'kuantitas': new_quantity}})
        # cart_items = list(cart_items)
        # for cart_item in cart_items:
        order_history = {
            'user_id': str(selected_user_id),
            'items': cart_items,
            # 'total_price': sum(item['total_harga_produk'] for item in cart_items),
            'total_price' : total_price,
            'order_date': datetime.today(),
        }
        history_purchase.insert_one(order_history)        
        # Hapus semua produk dari keranjang untuk user yang sedang login
        cart_collection.delete_many({'user_id': str(selected_user_id)})

        # Di sini Anda bisa menambahkan logika untuk pembayaran atau konfirmasi pesanan
        # Misalnya, menyimpan pesanan ke dalam database atau melakukan proses pembayaran
        
        # Contoh: Simpan pesanan ke dalam database atau lakukan proses pembayaran
        
        # Setelah selesai, redirect ke halaman yang sesuai (misalnya halaman konfirmasi atau halaman utama)
        return redirect(reverse('order_confirmation/'))  # Ganti 'order_confirmation' dengan URL yang sesuai
        
    # Jika request method bukan POST, bisa tambahkan logika sesuai kebutuhan
    return HttpResponse('Error: Invalid request method.')  # Atau tampilkan pesan kesalahan lainnya jika perlu

def orderConfirmation(request):
    return render(request, 'pelanggan/order_confirmation.html', {})