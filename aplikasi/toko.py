import datetime
from bson import ObjectId
from django.shortcuts import render, redirect
from .models import product_collection, user_collection, cart_collection, \
    supplier_product, sales_request, history_request, sales_product, sales_history
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
        products = sales_product.find({'kategori': selected_category, 'sales_id':str(user_log['_id'])})
        products = list(products)
    else:
        products = sales_product.find()
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
            'quantity': quantity,
            'category': str(product['kategori']),
            'sales_id': str(user_log['_id']),
            'status': 'pending',        
            'date': datetime.datetime.today(),
        }
        
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