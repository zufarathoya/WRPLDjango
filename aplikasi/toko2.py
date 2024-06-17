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

def req_pelanggan(request):
    user_log = user_collection.find_one({'is_login': True})
    if not user_log or user_log['category'] != 'toko':
        return redirect(reverse('login/'))
    
    product = sales_history.find({'sales_id':str(user_log['_id']), 'status': {'$nin': ['delivered', 'rejected']} })
    product = list(product)

    product.sort(key=lambda r: r['order_date'], reverse=True)
    context = {
        'products': product,
    }
    return render(request, 'toko/sales.html', context)

def terima(request):
    user_log = user_collection.find_one({'is_login': True})
    # if not user_log or user_log['category'] != 'toko':
    #     return redirect(reverse('login/'))
    
    if request.method == 'POST':
        request_id = request.POST.get('acc')
        reject = request.POST.get('reject')
        if reject:
            tolak(request)
        if request_id:
            sales_history.update_one({
                'order_id': str(request_id),
                'sales_id': str(user_log['_id'])
            }, {
                '$set': {'status': 'delivered'}
            })
            product_hist = sales_history.find({'order_id': request_id})
            product_hist = list(product_hist)
            print(len(product_hist))
            i = 0
            for product in product_hist:
                if product.get('status') == 'delivered':
                    i+=1
            print(len(product_hist), i)
            if i == len(product_hist):
                product_hist_one = sales_history.find_one({'order_id': request_id})
                delivery_price = 0
                if str(product_hist_one['location']).lower() == 'jakarta':
                    delivery_price = 20000
                elif str(product_hist_one['location']).lower() == 'semarang':
                    delivery_price = 10000
                elif str(product_hist_one['location']).lower() == 'surabaya':
                    delivery_price = 15000
                product_hist = sales_history.find({'order_id': request_id})
                # product_hist = dict(product_hist)
                delivery_req.insert_one({
                    'order_id': request_id,
                    # 'items': product_hist,
                    'status': 'pending',
                    'date': datetime.today(),
                    'location': product_hist_one['location'],
                    'ongkir': delivery_price,
                })
                product = sales_product.find_one({'_id':ObjectId(product_hist_one['product_id']),'sales_id':str(user_log['_id'])})
                # product = sales_product.find_one({'_id':ObjectId(product_hist['product_id'])})
                new_quantity = int(product['stok']) - product_hist_one['quantity']
                sales_product.update_one({'_id':ObjectId(product_hist_one['product_id']), 'sales_id':str(user_log['_id'])},{
                    '$inc': {'stock':-product_hist_one['quantity']}
                })
            return redirect(reverse('sales/'))
    return redirect(reverse('sales/'))

def tolak(request):
    user_log = user_collection.find_one({'is_login': True})
    # if not user_log or user_log['category'] != 'toko':
    #     return redirect(reverse('login/'))
    
    if request.method == 'POST':
        request_id = request.POST.get('reject')
        if request_id:
            sales_history.update_one(
                {'order_id': request_id},
                {'$set': {'status': 'rejected'}}
            )
            product_hist = sales_history.find_one({'order_id': request_id})
            sales_history.update_one({
                'order_id': request_id
            }, {
                '$set': {'status': 'rejected'}
            })
            BankAccount.update_one({
                'user_id': product_hist['user_id']
            }, {
                '$inc': {'saldo': product_hist['total_price']}
            })
            return redirect(reverse('req_pelanggan/'))
    return redirect(reverse('req_pelanggan/'))