from pyexpat.errors import messages
import uuid
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from .models import cart_collection, product_collection, delivery_req, \
    history_purchase, user_collection, purchase, sales_product, sales_history, \
    BankAccount, TopUpHistory
from bson import ObjectId
from datetime import datetime
from midtransclient import Snap
from .transaction import create_transaction
from django.contrib.auth.decorators import login_required

def bank(request):
    user_log = user_collection.find_one({'is_login':True})
    if not user_log or user_log['category'] != 'bank':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect(reverse('login/'))
    return render(request, 'bank/base.html', {})

def transaction_history(request):
    user_log = user_collection.find_one({'is_login':True})
    if not user_log or user_log['category'] != 'bank':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect(reverse('login/'))
    # print(user_id)
    transactions = TopUpHistory.find()
    transactions = list(transactions)
    for transaction in transactions:
        transaction['id'] = transaction['_id']
    # transactions.sort(key=lambda transaction: transaction['order_date'], reverse=True)
    context = {
        'transactions': transactions,
    }
    return render(request, 'bank/history.html', context)
