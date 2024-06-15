import datetime
from bson import ObjectId
from django.shortcuts import render, redirect
from .models import product_collection, user_collection, cart_collection, delivery_req
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

    requests = delivery_req.find()
    requests = list(requests)

    # Avoid reusing the variable name 'request' inside the loop
    for req in requests:
        req['id'] = req['_id']

    context = {
        'requests': requests,
    }

    return render(request, 'delivery/pesanan.html', context)