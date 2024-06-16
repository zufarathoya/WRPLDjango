import datetime
from bson import ObjectId
from django.shortcuts import render, redirect
from .models import product_collection, user_collection, cart_collection, \
    supplier_product, sales_request, history_request, sales_product, sales_history, \
    delivery_req, BankAccount
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

def show_product(request):
    user_log = user_collection.find_one({'is_login':True})
    if not user_log or user_log['category'] != 'toko':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect(reverse('login/'))

    categories = sales_product.distinct('kategori')
    selected_category = request.GET.get('kategori', '')

    if selected_category:
        products = sales_product.find({
            'kategori': selected_category,
            'sales_id':str(user_log['_id'])
        })
        products = list(products)
    else:
        products = sales_product.find({
            'sales_id':str(user_log['_id'])
        })
        products = list(products)

    for product in products:
        product['id'] = product['_id']

    context = {
        'products': products,
        'categories': categories,
        'selected_category': selected_category,
        'user':user_log['_id'],
    }

    return render(request, 'toko/show_product.html', context)

def action_request(request):
    user_log = user_collection.find_one({'is_login':True})
    if not user_log or user_log['category'] != 'toko':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect(reverse('login/'))

    if request.method == 'POST':
        product_id = request.POST.get('selected_product_id')
        quantity = int(request.POST.get('stock'))

        # product = supplier_product.find_one({'_id': ObjectId(product_id)})
        product = supplier_product.find_one({'nama': product_id})

        if not product:
            messages.error(request, 'Product not found.')
            return redirect(reverse('show_product/'))
        
        if quantity > product['stok']:
            messages.error(request, 'Quantity exceeds stock.')
            return redirect(reverse('show_product/'))

        # user = user_collection.find_one({'is_login': True})

        # if not user:
        #     messages.error(request, 'User not found.')
        #     return redirect(reverse('login/'))

        record = {
            'product_id': str(product['_id']),
            'product_name': str(product['nama']),
            'suplier_id': str(product['suplier_id']),
            'total harga': quantity * int(product['harga']),
            'quantity': quantity,
            'category': str(product['kategori']),
            'sales_id': str(user_log['_id']),
            'status': 'pending',        
            'date': datetime.datetime.today(),
        }
        
        saldo = BankAccount.find_one({
            'user_id': str(user_log['_id'])
        })

        if saldo['saldo'] < record['total harga']:
            messages.error(request, 'Insufficient balance.')
            return redirect(reverse('show_product/'))

        BankAccount.update_one({
            'user_id': str(user_log['_id'])
        },
        {
            '$inc': {'saldo': -record['total harga']}
        })

        sales_request.insert_one(record)

        sales_hist = sales_request.find_one({'product_id': str(product['_id'])})
        record['request_id'] = str(sales_hist['_id'])

        history_request.insert_one(record)

        messages.success(request, 'Product has been request.')
        return redirect(reverse('show_product/'))

    return redirect(reverse('request_toko/'))

def show_request_product(request):
    user_log = user_collection.find_one({'is_login':True})
    if not user_log or user_log['category'] != 'toko':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect(reverse('login/'))
    
    products_names = supplier_product.distinct('nama')
    products_names = list(products_names)
    selected_product = request.GET.get('product', '')
    if selected_product:
        products = supplier_product.find_one({'nama': selected_product})
        # products = products[0]

    else:
        products = supplier_product.find_one()
        # products = products[0]

    products["id"] = products["_id"]
    context = {
        'products_names': products_names,
        'products': products,
        'selected_product': selected_product,
    }
    
    return render(request, 'toko/request.html', context)

def show_all_request(request):
    user_log = user_collection.find_one({'is_login':True})
    if not user_log or user_log['category'] != 'toko':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect(reverse('login/'))

    reqs = history_request.find({'sales_id': str(user_log['_id'])})
    reqs = list(reqs)

    reqs.sort(key=lambda r: r['date'], reverse=True)

    for req in reqs:
        req['id'] = req['_id']

    context = {
        'items': reqs
    }

    return render(request, 'toko/request_history.html', context)

def sell_history(request):
    user_log = user_collection.find_one({'is_login':True})
    if not user_log or user_log['category'] != 'toko':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect(reverse('login/'))

    reqs = sales_history.find({'sales_id': str(user_log['_id'])})
    reqs = list(reqs)

    for req in reqs:
        req['id'] = req['_id']

    context = {
        'daftar': reqs
    }

    return render(request, 'toko/sales_history.html', context)

def status_pengiriman(request):
    user_log = user_collection.find_one({'is_login':True})
    if not user_log or user_log['category'] != 'toko':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect(reverse('login/'))
    
    req = delivery_req.find({'sales_id':str(user_log['_id'])})
    req = list(req)
    barang = {}

    requ = delivery_req.find()
    for r in requ:
        # Check if 'item' key exists and is not None
        if 'item' in r and r['item'] is not None and len(r['item']) > 0:
            # Iterate through all items in the 'item' list
            for barangs in r['item']:
                # Check if the 'sales_id' matches 'user_log' '_id'
                if barangs['sales_id'] == str(user_log['_id']):
                    # Store the item in the 'barang' dictionary with 'order_id' as the key
                    barang[r['order_id']] = {
                        'barangs': barangs,
                        'date': r['date'],
                        'status': r['status']
                    }

    req.sort(key=lambda r: r['date'], reverse=True)

    context = {
        'requests': req,
        'barangs': barang,
    }

    return render(request, 'toko/status.html', context)