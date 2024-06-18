import datetime
from bson import ObjectId
from django.shortcuts import render, redirect
from .models import product_collection, user_collection, cart_collection, delivery_req, sales_product, \
    history_request, sales_request, supplier_product
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

def show_request(request):
    # Ensure 'request' is an instance of HttpRequest
    if not isinstance(request, HttpRequest):
        return HttpResponse("Invalid request object", status=400)

    user_log = user_collection.find_one({'is_login': True})
    
    if not user_log or user_log['category'] != 'delivery':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect(reverse('login/'))

    requests = delivery_req.find({'status': {'$nin': ['done', 'rejected']}})
    requests = list(requests)

    # Avoid reusing the variable name 'request' inside the loop
    for req in requests:
        req['id'] = req['_id']
    
    requests.sort(key=lambda req: req['date'], reverse=True)

    context = {
        'requests': requests,
    }

    return render(request, 'delivery/pesanan.html', context)

def accept_delivery(request):
    # Ensure 'request' is an instance of HttpRequest
    if not isinstance(request, HttpRequest):
        return HttpResponse("Invalid request object", status=400)

    user_log = user_collection.find_one({'is_login': True})
    
    if not user_log or user_log['category'] != 'delivery':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect(reverse('login/'))

    if request.method == 'POST':
        selected_id = request.POST.get('accept')
        reject = request.POST.get('reject')
        if reject:
            tolak(request)
        # print(selected_id)

        # delivery = delivery_req.find_one({'_id': ObjectId(selected_id)})
        delivery = delivery_req.find_one({'order_id': str(selected_id)})

        if delivery:
            if delivery['status'] == 'pending':
                # delivery_req.update_one({'_id': ObjectId(selected_id)}, {
                delivery_req.update_one({'order_id': str(selected_id)}, {
                    '$set': {'status': 'accept'}
                })
            elif delivery['status'] == 'accept':
                # delivery_req.update_one({'_id': ObjectId(selected_id)}, {
                delivery_req.update_one({'order_id': str(selected_id)}, {
                    '$set': {'status': 'done'}
                })
                product_hist = history_request.find_one({'request_id': str(delivery['order_id'])})
                if product_hist:
                    sales_req = history_request.find_one({'request_id': str(delivery['order_id'])})
                    product = sales_product.find_one({'_id':ObjectId(sales_req['product_id'])})
                    if product:
                        sales_product.update_one(
                            {'_id': ObjectId(product_hist['product_id'])},
                            {'$inc': {'stok': product_hist['quantity']}}
                        )
                    else:
                        from_supp = supplier_product.find_one({'_id':ObjectId(product_hist['product_id'])})
                        update = {
                            '_id': ObjectId(from_supp['_id']),
                            'merek': from_supp['merek'],
                            'kategori': from_supp['kategori'],
                            'deskripsi': from_supp['deskripsi'],
                            'harga': int(from_supp['harga']),
                            'nama': product_hist['product_name'],
                            'sales_id': str(product_hist['sales_id']),
                            'stok': product_hist['quantity'],
                            'date': product_hist['date'],
                        }
                        sales_product.insert_one(update)

            messages.success(request, 'Delivery has been accepted successfully.')
            return redirect(reverse('delivery_req/'))

    return redirect(reverse('delivery_req/'))

def tolak(request):
    if request.method == 'POST':
        selected_id = request.POST.get('reject')
        # print(selected_id)

        # delivery = delivery_req.find_one({'_id': ObjectId(selected_id)})
        delivery = delivery_req.find_one({'order_id': str(selected_id)})

        if delivery:
            if delivery['status'] == 'pending':
                # delivery_req.update_one({'_id': ObjectId(selected_id)}, {
                delivery_req.update_one({'order_id': str(selected_id)}, {
                    '$set': {'status': 'rejected'}
                })
            elif delivery['status'] == 'accept':
                # delivery_req.update_one({'_id': ObjectId(selected_id)}, {
                delivery_req.update_one({'order_id': str(selected_id)}, {
                    '$set': {'status': 'pending'}
                })

            messages.success(request, 'Delivery has been rejected successfully.')
            return redirect(reverse('delivery_req/'))

    return redirect(reverse('delivery_req/'))

def history_pesanan(request):
        # Ensure 'request' is an instance of HttpRequest
    if not isinstance(request, HttpRequest):
        return HttpResponse("Invalid request object", status=400)

    user_log = user_collection.find_one({'is_login': True})
    
    if not user_log or user_log['category'] != 'delivery':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect(reverse('login/'))

    requests = delivery_req.find()
    requests = list(requests)

    # Avoid reusing the variable name 'request' inside the loop
    for req in requests:
        req['id'] = req['_id']
    
    requests.sort(key=lambda req: req['date'], reverse=True)

    context = {
        'requests': requests,
    }

    return render(request, 'delivery/history_pesanan.html', context)