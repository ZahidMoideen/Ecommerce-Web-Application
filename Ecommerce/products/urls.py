from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from.import views

urlpatterns = [
    path('',views.index,name="index"),
    path('list/products/',views.list_products,name="list_products"),
    path('product/details/<pk>',views.product_details,name="product_details" ),
    path('dashboard/',views.admin_dashboard,name="admin_dashboard" ),
    path('add/products/',views.add_products,name="add_products" ),
    path('all/products/',views.all_products,name="all_products" ),
    path('update/products/<int:id>',views.update_products,name="update_products" ),
    path('delete/products/<int:id>',views.delete_products,name="delete_products" ),

]




