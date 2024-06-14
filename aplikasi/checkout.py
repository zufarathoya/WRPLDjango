import uuid
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from .models import cart_collection, product_collection, \
    history_purchase, user_collection, purchase
from bson import ObjectId
from datetime import datetime
from midtransclient import Snap
from .transaction import create_transaction
from django.contrib.auth.decorators import login_required


# @login_required(login_url='login/')
def checkout(request):
    if request.method == 'POST':
        # selected_user_id = request.POST.get('_user_id')
        # total_price = request.POST.get('total_harga')

        user_id_ = user_collection.find_one({'is_login':True})
        user_id_ = user_id_['_id']
        print(user_id_)
        
        cart_items = cart_collection.find({'user_id': str(user_id_)})
        cart_items = list(cart_items)
        
        for item in cart_items:
            product_id = item['product_id']
            cart_quantity = item['kuantitas']
            
            product = product_collection.find_one({'_id': ObjectId(product_id)})
            if product:
                
                new_quantity = int(product['stok']) - cart_quantity
                product_collection.update_one({'_id': ObjectId(product_id)}, {'$set': {'stok': new_quantity}})
        # cart_items = list(cart_items)
        # for cart_item in cart_items:
        order_history = {
            'user_id': str(user_id_),
            'items': cart_items,
            'total_price': sum(item['total_harga_produk'] for item in cart_items),
            # 'total_price' : total_price,
            'order_date': datetime.today(),
        }
        
        history_purchase.insert_one(order_history)
        purchase.insert_one(order_history)

        # order = history_purchase.find_one({'user_id':str(user_id_)})
        order = purchase.find_one({'user_id':str(user_id_)})

        order_id = order['_id']

        purchase.delete_one({'user_id':str(user_id_)})
        
        order_dict = {
            'order_id': str(order_id),
            'user_id': user_id_,
            'total_price': sum(item['total_harga_produk'] for item in cart_items),
            'order_date': datetime.today(),
        }
        
        redirect_url = create_transaction(request, order_dict)
        # Hapus semua produk dari keranjang untuk user yang sedang login
        cart_collection.delete_many({'user_id': str(user_id_)})

        return redirect(redirect_url)  # Ganti 'order_confirmation' dengan URL yang sesuai
        
    return HttpResponse('Error: Invalid request method.')

def orderConfirmation(request):
    return render(request, 'pelanggan/order_confirmation.html', {})