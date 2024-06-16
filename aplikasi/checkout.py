import uuid
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from .models import cart_collection, product_collection, delivery_req, \
    history_purchase, user_collection, purchase, sales_product, sales_history, \
    BankAccount
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
        location = request.POST.get('location')
        user_id_ = user_collection.find_one({'is_login':True})
        user_id_ = user_id_['_id']
        print(user_id_)
        
        cart_items = cart_collection.find({'user_id': str(user_id_)})
        cart_items = list(cart_items)
        
        for item in cart_items:
            product_id = item['product_id']
            cart_quantity = item['kuantitas']
            
            product = sales_product.find_one({'_id': ObjectId(product_id)})
            if product:
                sales_id = product['sales_id']
                item['sales_id'] = sales_id

                sales = {
                    'sales_id': sales_id,
                    'product_id': product_id,
                    'quantity': cart_quantity,
                    'name': product['nama'],
                    'price': product['harga'],
                    'total_price': item['total_harga_produk'],
                    'user_id': str(user_id_),
                    'status': 'pending',
                    'payment_method': 'midtrans',
                    'order_id': str(uuid.uuid4()),
                    'order_date': datetime.today()
                }
                sales_history.insert_one(sales)
                new_quantity = int(product['stok']) - cart_quantity
                sales_product.update_one({'_id': ObjectId(product_id)}, {'$set': {'stok': new_quantity}})
        # cart_items = list(cart_items)
        # for cart_item in cart_items:
        delivery_price = 0
        if str(location).lower() == 'jakarta':
            delivery_price = 20000
        elif str(location).lower() == 'semarang':
            delivery_price = 10000
        elif str(location).lower() == 'surabaya':
            delivery_price = 15000

        order_history = {
            'user_id': str(user_id_),
            'items': cart_items,
            'total_price': sum(item['total_harga_produk'] for item in cart_items),
            # 'total_price' : total_price,
            'order_date': datetime.today(),
            'status': 'pending',
            'location': location,
            'ongkir':delivery_price,
        }

        BankAccount.update_one(
            {'user_id':str(user_id_)},
            {
                '$inc': {
                    'saldo':-(int(sum(item['total_harga_produk'] for item in cart_items)) + delivery_price)
                    }
                }
            )

        purchase.insert_one(order_history)

        # order = history_purchase.find_one({'user_id':str(user_id_)})
        order = purchase.find_one({'user_id':str(user_id_)})

        order_id = order['_id']
        order_history['order_id'] = order_id
        
        # sales_history.insert_one(order_history)
        history_purchase.insert_one(order_history)

        # purchase.delete_one({'user_id':str(user_id_)})
        delivery_req.insert_one({
            'user_id': str(user_id_),
            'order_id': str(order_id),
            'item': cart_items,
            'status': 'pending',
            'date': datetime.today(),
            'ongkir': delivery_price
        })

        order_dict = {
            'order_id': str(order_id),
            'user_id': user_id_,
            'total_price': sum(item['total_harga_produk'] for item in cart_items),
            'order_date': datetime.today(),
            'ongkir': delivery_price
        }
        
        redirect_url = create_transaction(request, order_dict)

        cart_collection.delete_many({'user_id': str(user_id_)})

        return redirect(redirect_url)  # Ganti 'order_confirmation' dengan URL yang sesuai
        
    return HttpResponse('Error: Invalid request method.')

def orderConfirmation(request):
    return render(request, 'pelanggan/order_confirmation.html', {})