import uuid
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from .models import BankAccount, TopUpHistory, cart_collection, product_collection, history_purchase, user_collection
from bson import ObjectId
from datetime import datetime
from midtransclient import Snap


def checkout(request):
    if request.method == 'POST':
        # Ambil data yang dikirim dari form
        selected_user_id = request.POST.get('_user_id')
        total_price = request.POST.get('total_harga')
        user_id_ = user_collection.find_one({'is_login':True})
        user_id_ = user_id_['_id']
        # Ambil semua item dari keranjang untuk user yang sedang login
        cart_items = cart_collection.find({'user_id': str(user_id_)})
        cart_items = list(cart_items)
        # Kurangi kuantitas produk di product_collection
        for item in cart_items:
            product_id = item['product_id']
            cart_quantity = item['kuantitas']
            
            # Cari produk di product_collection
            product = product_collection.find_one({'_id': ObjectId(product_id)})
            if product:
                # Kurangi kuantitas produk
                new_quantity = int(product['stok']) - cart_quantity
                product_collection.update_one({'_id': ObjectId(product_id)}, {'$set': {'stok': new_quantity}})
        # cart_items = list(cart_items)
        # for cart_item in cart_items:
        order_history = {
            'user_id': user_id_,
            'items': cart_items,
            'total_price': sum(item['total_harga_produk'] for item in cart_items),
            # 'total_price' : total_price,
            'order_date': datetime.today(),
        }
        
        history_purchase.insert_one(order_history)

        order = history_purchase.find_one({'user_id':user_id_})
        order_id = order['_id']
        
        order_dict = {
            'order_id': str(order_id),
            'user_id': user_id_,
            'total_price': total_price,
            'order_date': datetime.today(),
        }

        def create_transaction(request, dict):
            # gross_amount = request.POST.get('gross_amount')
            # user_id = request.POST.get('user_id')
            snap = Snap(
                is_production=False,
                server_key='server-key',  
                client_key='client-key'
            )
            # order_id = str(uuid.uuid4()) 

            param = {
                "transaction_details": {
                    "order_id": order_dict['order_id'],
                    "gross_amount": order_dict['total_price'],
                },
                "credit_card":{
                    "secure" : True
                }
            }

            transaction = snap.create_transaction(param)
            print(transaction)
            TopUpHistory.objects.create(
                bank_account=BankAccount,
                transaction_type='P',
                amount = order_dict['total_price'],
                order_id = order_dict['order_id'], 
                user_id = order_dict['user_id'],
            )
            return redirect(transaction['redirect_url'])
        
        create_transaction(request, order_dict)
        # Hapus semua produk dari keranjang untuk user yang sedang login
        cart_collection.delete_many({'user_id': str(user_id_)})

        # Di sini Anda bisa menambahkan logika untuk pembayaran atau konfirmasi pesanan
        # Misalnya, menyimpan pesanan ke dalam database atau melakukan proses pembayaran
        
        # Contoh: Simpan pesanan ke dalam database atau lakukan proses pembayaran
        
        # Setelah selesai, redirect ke halaman yang sesuai (misalnya halaman konfirmasi atau halaman utama)
        return redirect(reverse('order_confirmation/'))  # Ganti 'order_confirmation' dengan URL yang sesuai
        
    # Jika request method bukan POST, bisa tambahkan logika sesuai kebutuhan
    return HttpResponse('Error: Invalid request method.')  # Atau tampilkan pesan kesalahan lainnya jika perlu

def orderConfirmation(request):
    return render(request, 'pelanggan/order_confirmation.html', {})
