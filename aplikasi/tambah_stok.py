from bson import ObjectId
from django.shortcuts import get_object_or_404, render, redirect
from .models import product_collection, user_collection
from django.contrib import messages
from django.urls import reverse

def addStock(request):
    if request.method == 'POST':
        selected_id = request.POST.get('selected_product_id')
        stock = int(request.POST.get('stock'))  # Ensure stock is an integer

        # Find the product based on the ID
        # product = product_collection.find_one({'_id': ObjectId(selected_id)})
        product = product_collection.find_one({'name': selected_id})

        if product:
            # Update the product's stock
            # product_collection.update_one({'_id': ObjectId(selected_id)}, {
            #     '$inc': {'stok': stock}
            # })
            product_collection.update_one({'name': selected_id}, {
                '$inc': {'stok': stock}
            })

            messages.success(request, 'Stock has been added successfully.')
            return redirect(reverse('gudang_show/'))

    return redirect(reverse('gudang_show/'))

def show_product(request):
    # Get all unique categories from the product collection
    categories = product_collection.distinct('kategori')

    # Get the selected category from the GET request
    selected_category = request.GET.get('kategori', '')

    if selected_category:
        products = product_collection.find({'kategori': selected_category})
        products = list(products)
    else:
        products = product_collection.find()
        products = list(products)

    for product in products:
        product['id'] = product['_id']

    context = {
        'products': products,
        'categories': categories,
        'selected_category': selected_category,
    }

    return render(request, 'gudang/show_product.html', context)

def show_add_stock(request):
    products_names = product_collection.distinct('nama')
    products_names = list(products_names)
    selected_product = request.GET.get('product', '')
    if selected_product:
        products = product_collection.find_one({'nama': selected_product})
        # products = products[0]

    else:
        products = product_collection.find_one()
        # products = products[0]

    products["id"] = products["_id"]
    context = {
        'products_names': products_names,
        'products': products,
        'selected_product': selected_product,
    }
    
    return render(request, 'gudang/tambah_stok.html', context)

def tambah_produk(request):
    if request.method == 'POST':
        nama = request.POST.get('nama')
        kategori = request.POST.get('kategori')
        harga = request.POST.get('harga')
        stok = request.POST.get('stok')
        deskripsi = request.POST.get('deskripsi')

        chek = product_collection.find({'nama':nama})
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

        product_collection.insert_one(product)

        messages.success(request, 'Product added successfully.')
        return redirect(reverse('gudang_show/'))

    return render(request, 'gudang/tambah_produk.html')