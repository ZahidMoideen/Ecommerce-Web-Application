from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render, redirect
from .models import Customer
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def account(request):
    if request.method == 'POST':
        if 'register' in request.POST:
            # Handle registration
            username = request.POST.get('username')
            password = request.POST.get('password')
            email = request.POST.get('email')
            address = request.POST.get('address')
            phone = request.POST.get('phone')

            if User.objects.filter(username=username).exists():
                error_message = "Username already exists. Please choose a different one."
                return render(request, 'web/account.html', {'error_message': error_message})

            try:
                user = User.objects.create_user(username=username, email=email, password=password)
                customer = Customer.objects.create(name=username,user=user, phone=phone, address=address)
                messages.success(request, 'Registration successful. You can now log in.')
            except IntegrityError:
                error_message = "An error occurred while creating the user. Please try again later."
                return render(request, 'web/account.html', {'error_message': error_message})

        elif 'login' in request.POST:
            # Handle login
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.error(request, "Invalid username or password. Please try again.")

    return render(request, 'web/account.html')

def sign_out(request):
    logout(request)
    return redirect('index')


@login_required(login_url='account')
def profile(request):
    # Assuming you have a way to identify the logged-in user
    user = request.user
    # Assuming Customer_profile is the related name for the Customer model
    customer = user.Customer_profile
    return render(request, 'web/profile.html', {'customer': customer})