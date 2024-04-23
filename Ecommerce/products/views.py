from django.shortcuts import render,redirect,get_object_or_404
from . models import Product
from django.core.paginator import Paginator
from .forms import ProductForm
from django.contrib import messages
# Create your views here.

def index(request):
    featured_products=Product.objects.order_by('priority')[:4]
    latest_products=Product.objects.order_by('-id')[:4]
    context={
        'featured_products':featured_products,
        'latest_products':latest_products
    }
    return render(request,'web/index.html',context)

def list_products(request):
    page=1
    if request.GET:
        page=request.GET.get('page',1)
    product_list=Product.objects.order_by('-priority')
    product_paginator=Paginator(product_list,4)
    product_list=product_paginator.get_page(page)
    context={'products':product_list}
    return render(request,'web/Products.html',context)

def product_details(request,pk):
    product=Product.objects.get(pk=pk)
    context={'product':product}
    return render(request,'web/product_details.html',context)

def admin_dashboard(request):
    return render(request,'web/dashboard/dashboard.html')

def add_products(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product has been successfully added.')
            return redirect('add_products')
    else:
        form = ProductForm()
    return render(request, 'web/dashboard/add_products.html', {'form': form})


def all_products(request):
    page=1
    if request.GET:
        page=request.GET.get('page',1)
    product_list=Product.objects.order_by('-priority')
    product_paginator=Paginator(product_list,15)
    product_list=product_paginator.get_page(page)
    context={'products':product_list}
    return render(request,'web/dashboard/all_products.html',context)


def update_products(request, id):
    product = Product.objects.get(pk=id)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('all_products')
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'web/dashboard/product_update.html', {'product': product})


def delete_products(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully.')
        return redirect('all_products')
    else:
        return render(request, 'web/dashboard/product_delete.html', {'product': product})
    