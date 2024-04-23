from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from.import views

urlpatterns = [
    path('account/',views.account,name="account"),
    path('signout/',views.sign_out,name="sign_out"),
    path('profile/', views.profile, name='profile'),
]


    




