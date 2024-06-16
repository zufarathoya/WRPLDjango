import datetime
from bson import ObjectId
from django.shortcuts import get_object_or_404, render, redirect
from .models import user_collection, sales_request, \
            history_request, sales_product, supplier_product, delivery_req, supplier_product_history
from django.contrib import messages
from django.urls import reverse
from  datetime import datetime
from .gudang import tolak

def addStock(request):
    user_log = user_collection.find_one({'is_login':True})
    if not user_log or user_log['category'] != 'gudang':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect(reverse('login/'))
    
    if request.method == 'POST':
        selected_id = request.POST.get('selected_product_id')
        stock = int(request.POST.get('stock'))  # Ensure stock is an integer

        # Find the product based on the ID
        # product = product_collection.find_one({'_id': ObjectId(selected_id)})
        product = supplier_product.find_one({
            'nama': selected_id, 'suplier_id':str(user_log['_id'])
        })

        if product:
            # Update the product's stock
            # product_collection.update_one({'_id': ObjectId(selected_id)}, {
            #     '$inc': {'stok': stock}
            # })
            supplier_product.update_one({
                'nama': selected_id, 'suplier_id':str(user_log['_id']) }
                , {
                '$inc': {'stok': stock}
            })

            supplier_product_history.insert_one({
                'tipe':'Add Stock',
                'harga':int(product['harga']),
                'product_id': str(product['_id']),
                'kuantitas': stock,
                'nama': product['nama'],
                'merek': product['merek'],
                'kategori': product['kategori'],
                'suplier_id':str(user_log['_id']),
                'tanggal': datetime.today(),
            })

            messages.success(request, 'Stock has been added successfully.')
            return redirect(reverse('gudang_show/'))

    return redirect(reverse('gudang_show/'))

def add_product(request):
    user_log = user_collection.find_one({'is_login':True})
    if not user_log or user_log['category'] != 'gudang':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect(reverse('login/'))

    if request.method == 'POST':
        quantity = int(request.POST.get('stok'))
        nama = request.POST.get('nama')
        merek = request.POST.get('merek')
        kategori = request.POST.get('kategori')
        deskripsi = request.POST.get('deskripsi')
        harga = request.POST.get('harga')

        supplier_product.insert_one({
            'harga': harga,
            'stok': quantity,
            'nama': nama,
            'merek': merek,
            'deskripsi': deskripsi,
            'kategori':kategori,
            'suplier_id':str(user_log['_id']),
        })

        supplier_product_history.insert_one({
            'tipe': 'Add Product',
            'kuantitas': quantity,
            'nama': nama,
            'merek': merek,
            'kategori': kategori,
            'tanggal': datetime.today(),
            'suplier_id':str(user_log['_id']),
        })

        messages.success(request, 'Request has been sent.')
        return redirect(reverse('gudang_show/'))
        
    return redirect(reverse('gudang_show/'))

def show_product(request):
    user_log = user_collection.find_one({'is_login':True})
    if not user_log or user_log['category'] != 'gudang':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect(reverse('login/'))

    categories = supplier_product.distinct('kategori')

    selected_category = request.GET.get('kategori', '')

    if selected_category:
        products = supplier_product.find({'kategori': selected_category, 'suplier_id':str(user_log['_id'])})
        products = list(products)
    else:
        products = supplier_product.find({'suplier_id':str(user_log['_id'])})
        products = list(products)

    for product in products:
        product['id'] = product['_id']

    context = {
        'products': products,
        'categories': categories,
        'selected_category': selected_category,
    }

    return render(request, 'gudang/show_product.html', context)

def product_history(request):
    user_log = user_collection.find_one({'is_login':True})
    if not user_log or user_log['category'] != 'gudang':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect(reverse('login/'))

    product = supplier_product_history.find({'suplier_id':str(user_log['_id'])})
    product = list(product)
    for prod in product:
        prod['id'] = prod['_id']

    product.sort(key=lambda r: r['tanggal'], reverse=True)

    context = {
        'items': product,
    }

    return render(request, 'gudang/product_history.html', context)

def show_add_stock(request):
    user_log = user_collection.find_one({'is_login':True})
    if not user_log or user_log['category'] != 'gudang':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect(reverse('login/'))
    
    supplier_product_name = supplier_product.find({'suplier_id':str(user_log['_id'])})
    products_names = supplier_product_name.distinct('nama')
    products_names = list(products_names)
    selected_product = request.GET.get('product', '')
    if selected_product:
        products = supplier_product.find_one({
            'nama': selected_product, 
            'suplier_id':str(user_log['_id'])
        })
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
    
    return render(request, 'gudang/tambah_stok.html', context)

def tambah_produk(request):
    user_log = user_collection.find_one({'is_login':True})
    if not user_log or user_log['category'] != 'gudang':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect(reverse('login/'))


    if request.method == 'POST':
        nama = request.POST.get('nama')
        kategori = request.POST.get('kategori')
        harga = request.POST.get('harga')
        stok = request.POST.get('stok')
        deskripsi = request.POST.get('deskripsi')

        chek = supplier_product.find({'nama':nama})
        chek = list(chek)
        if chek:
            messages.error(request, 'Product already exists.')
            return redirect(reverse('gudang_show/'))

        product = {
            'nama': nama,
            'kategori': kategori,
            'harga': harga,
            'stok': stok,
            'deskripsi': deskripsi,
        }

        supplier_product.insert_one(product)

        messages.success(request, 'Product added successfully.')
        return redirect(reverse('gudang_show/'))

    return render(request, 'gudang/tambah_produk.html')

def sales_request_(request):
    user_log = user_collection.find_one({'is_login':True})
    if not user_log or user_log['category'] != 'gudang':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect(reverse('login/'))
    
    reqs = sales_request.find({'suplier_id' : str(user_log['_id'])})
    reqs = list(reqs)
    for req in reqs:
        req['id'] = req['_id'] 
    context = {
        'requests': reqs,
    }

    return render(request, 'gudang/permintaan.html', context)

def accept_request(request):
    user_log = user_collection.find_one({'is_login':True})
    if not user_log or user_log['category'] != 'gudang':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect(reverse('login/'))
    
    if request.method == 'POST':
        request_id = request.POST.get('acc')

        deny = request.POST.get('deny')
        if deny:
            tolak(request)
            return redirect(reverse('permintaan_toko/'))

        if request_id:
            history_request.update_one(
                {'request_id': request_id},
                {'$set': {'status': 'accepted'}}
            )
            product_hist = history_request.find_one({'request_id': request_id})

            messages.success(request, 'Request has been accepted.')
            
            sales_req = sales_request.find_one({'_id': ObjectId(request_id)})

            delivery_req.insert_one({
                'order_id': str(request_id),                
                'sales_id': product_hist['sales_id'],
                'suplier_id': product_hist['suplier_id'],
                'product_id': product_hist['product_id'],
                'product_name': product_hist['product_name'],
                'quantity': product_hist['quantity'],
                'status': 'pending',
                'date': datetime.today(),
            })

            deli = delivery_req.find()
            deli = list(deli)

            product = sales_product.find_one({'_id':ObjectId(sales_req['product_id'])})
            # product = sales_product.find_one({'_id':ObjectId(request_id)})
            supplier_product.update_one(
                {'_id': ObjectId(product_hist['product_id'])},
                {'$inc': {'stok': -product_hist['quantity']}}
            )
            supplier_product_history.insert_one({
                'request_id': sales_req['_id'],
                'tipe': 'Send to Sales',
                'product_id': sales_req['product_id'],
                'kuantitas': sales_req['quantity'],
                'nama': sales_req['product_name'],
                # 'kategori': product['category'],
                'tanggal': datetime.today(),
                'suplier_id':str(user_log['_id']),
            })

            sales_request.delete_one(
                {'_id': ObjectId(request_id)}
            )

            # if product:
            #     sales_product.update_one(
            #         {'_id': ObjectId(product_hist['product_id'])},
            #         {'$inc': {'stok': product_hist['quantity']}}
            #     )
            # else:
            #     from_supp = supplier_product.find_one({'_id':ObjectId(product_hist['product_id'])})
            #     update = {
            #         '_id': ObjectId(from_supp['_id']),
            #         'merek': from_supp['merek'],
            #         'kategori': from_supp['kategori'],
            #         'deskripsi': from_supp['deskripsi'],
            #         'harga': int(from_supp['harga']),
            #         'nama': product_hist['product_name'],
            #         'sales_id': product_hist['sales_id'],
            #         'stok': product_hist['quantity'],
            #         'date': product_hist['date'],
            #     }
            #     sales_product.insert_one(update)
        else:
            messages.error(request, 'Invalid request ID.')
    
    return redirect(reverse('permintaan_toko/'))

def status_pengiriman(request):
    user_log = user_collection.find_one({'is_login':True})
    if not user_log or user_log['category'] != 'gudang':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect(reverse('login/'))
    
    req = delivery_req.find({'suplier_id':str(user_log['_id'])})
    req = list(req)

    req.sort(key=lambda r: r['date'], reverse=True)

    context = {
        'requests': req,
    }

    return render(request, 'gudang/status.html', context)