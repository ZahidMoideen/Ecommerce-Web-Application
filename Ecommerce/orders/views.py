from django.shortcuts import render,redirect
from.models import Order,OrderedItem
from products.models import Product
from django.db.models import F
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash



# Create your views here.
@login_required(login_url='account')
def cart(request):
    user = request.user
    customer = user.Customer_profile  
    cart_obj, created = Order.objects.get_or_create(
        owner=customer,
        order_status=Order.CART_STAGE
    )
    context = {'cart': cart_obj}
    return render(request, 'web/cart.html', context)

@login_required(login_url='account')
def add_to_cart(request):
    if request.POST:
        user = request.user
        customer = user.Customer_profile  
        quantity = int(request.POST.get('quantity'))
        product_id = request.POST.get('product_id')
        cart_obj, created = Order.objects.get_or_create(
            owner=customer,
            order_status=Order.CART_STAGE
        )
        product = Product.objects.get(pk=product_id)
        
        # Check if the product already exists in the cart
        existing_item = OrderedItem.objects.filter(owner=cart_obj, product=product).first()
        if existing_item:
            # If it exists, update the quantity and price
            existing_item.quantity = F('quantity') + quantity
            existing_item.save()
        else:
            # If it doesn't exist, create a new entry
            ordered_item = OrderedItem.objects.create(
                product=product,
                owner=cart_obj,
                quantity=quantity
            )
    return redirect('cart')


@login_required(login_url='account')
def remove_cart_item(request,pk):
    item=OrderedItem.objects.get(pk=pk)
    if item:
        item.delete()
    return redirect('cart')

@login_required(login_url='account')
def checkout_cart(request): 
    if request.POST:
        try:
            user=request.user
            customer=user.Customer_profile
            total=float(request.POST.get('total'))
            order_obj=Order.objects.get(
                owner=customer,
                order_status=Order.CART_STAGE
            )
            if order_obj:
                order_obj.order_status=Order.ORDER_CONFIRMED
                order_obj.total_price=total
                order_obj.save()
                status_message="Your Order has been Successfully Processed,Your item is on the way to you"
                messages.success(request,status_message)
            else:
                status_message="Unable to process your Order,No items in cart"
                messages.success(request,status_message)
        except Exception as e:
                status_message="Unable to process your Order,No items in cart"
                messages.success(request,status_message)
        return redirect('cart')

@login_required(login_url='account')
def view_orders(request):
    user=request.user
    customer=user.Customer_profile
    all_orders=Order.objects.filter(owner=customer).exclude(order_status=Order.CART_STAGE)
    context={'orders':all_orders}
    return render(request,'web/order.html',context)




