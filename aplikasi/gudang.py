import datetime
from bson import ObjectId
from django.shortcuts import get_object_or_404, render, redirect
from .models import product_collection, user_collection, sales_request, \
            history_request, sales_product, supplier_product, delivery_req, \
            supplier_product_history, BankAccount
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from  datetime import datetime

def tolak(request):
    user_log = user_collection.find_one({'is_login':True})
    if not user_log or user_log['category'] != 'gudang':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect(reverse('login/'))
    
    if request.method == 'POST':
        request_id = request.POST.get('deny')
        if request_id:
            history_request.update_one(
                {'request_id': request_id},
                {'$set': {'status': 'rejected'}}
            )
            product_hist = history_request.find_one({'request_id': request_id})
            history_request.update_one({
                'request_id': request_id
            }, {
                '$set': {'status': 'rejected'}
            })
            
            sales_req = history_request.find_one({'order_id': ObjectId(request_id)})
            sales_request.delete_one(
                {'_id': ObjectId(request_id)}
            )
            print(request_id)
            BankAccount.update_one({
                'user_id': product_hist['sales_id']
            }, {
                '$inc': {'saldo': product_hist['total_price']}
            })

    return redirect(reverse('show_request/'))