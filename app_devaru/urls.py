from django.urls import path
from . import views
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('login')),  # ✅ Handle empty path by redirecting to login
    path('login/', views.login_view, name='login'),  
    path('home/', views.home_view, name='home'),  
    path('logout/', views.logout_view, name='logout'), 
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('register/', views.register_view, name='register'),
    path('add_item/', views.add_item, name='add_item'),
    path('add_item/', views.add_item, name='add_item'),
    path('add-customer/', views.add_customer, name='add_customer'),
    path('edit_item/<int:item_id>/', views.edit_item, name='edit_item'),
    path('delete_item_ajax/<int:item_id>/', views.delete_item_ajax, name='delete_item_ajax'),
    path('view-sales/', views.view_sales, name='view_sales'),
    path('print-sale/<int:sale_id>/', views.print_sale, name='print_sale'),  # new url
    path('print-customer/<int:customer_id>/', views.print_customer, name='print_customer'),
    path('products/', views.view_products, name='view_products'),
    path('autocomplete_search/', views.autocomplete_search, name='autocomplete_search'),
    path('edit-customer/<int:id>/', views.edit_customer, name='edit_customer'),
    path('delete-customer/<int:id>/', views.delete_customer, name='delete_customer'),



]









