from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from .models import JewelleryItem, Sale
from .forms import JewelleryItemForm
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomerForm  
from .models import Customer
from .models import JewelleryItem
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils import generate_barcode


# Login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if username == 'admin' and password == 'admin123':
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Admin user does not exist in the database.")
        else:
            messages.error(request, 'Only the admin can login.')
        return redirect('login')
    return render(request, 'login.html')



# Home view
@login_required
def home_view(request):
    total_items = JewelleryItem.objects.count()
    total_quantity = JewelleryItem.objects.aggregate(Sum('quantity'))['quantity__sum'] or 0
    total_sales = Sale.objects.aggregate(Sum('total_price'))['total_price__sum'] or 0
    return render(request, 'home.html', {
        'total_items': total_items,
        'total_quantity': total_quantity,
        'total_sales': total_sales
    })


# Logout view
def logout_view(request):
    logout(request)
    return redirect('login')


# Forgot Password & Register
def forgot_password_view(request):
    return render(request, 'forgot_password.html')


def register_view(request):
    return render(request, 'register.html')


# views.py
@login_required
def add_item(request):
    if request.method == 'POST':
        category = request.POST.get('category')
        name = request.POST.get('name')
        quantity = int(request.POST.get('quantity'))
        purity = request.POST.get('purity')
        weight = request.POST.get('weight')

        # Check if item with same category and name exists
        existing_item = JewelleryItem.objects.filter(
            category=category,
            name=name
        ).first()

        if existing_item:
            # Update quantity
            existing_item.quantity += quantity
            existing_item.purity = purity
            existing_item.weight = weight
            existing_item.save()

        else:
            # Create new item
            JewelleryItem.objects.create(
                category=category,
                name=name,
                quantity=quantity,
                purity=purity,
                weight=weight
            )

        return redirect('add_item')

    items = JewelleryItem.objects.all()

    for item in items:
        if not item.item_code:
            item.item_code = item.generate_item_code()
            item.save(update_fields=["item_code"])
        item.barcode = generate_barcode(item.item_code)

    return render(request, 'add_item.html', {
        'items': items,
        'button_label': 'Add Item'
    })




@login_required
def add_customer(request):

    if request.method == 'POST':
        form = CustomerForm(request.POST)

        if form.is_valid():
            customer = form.save(commit=False)

            try:
                item = JewelleryItem.objects.get(
                    name=customer.product,
                    category=customer.category
                )

                if item.quantity >= customer.quantity:
                    item.quantity -= customer.quantity
                    item.save()

                    customer.save()

                    messages.success(request, "Customer added and stock updated!")

                    return redirect('print_customer', customer_id=customer.id)

                else:
                    messages.error(
                        request,
                        f"Not enough stock! Available quantity: {item.quantity}"
                    )

            except JewelleryItem.DoesNotExist:
                messages.error(request, "Product not found in inventory!")

    status_filter = request.GET.get('status')

    customers = Customer.objects.all().order_by('-id')

    if status_filter:
        customers = customers.filter(status=status_filter)

    return render(request, 'add_customer.html', {
        'form': CustomerForm(),
        'customers': customers,
        'selected_status': status_filter
    })



def print_customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)

    item = JewelleryItem.objects.filter(
        name=customer.product,
        category=customer.category
    ).first()

    item_code = ''
    item_barcode = ''
    item_label = customer.product

    if item:
        if not item.item_code:
            item.item_code = item.generate_item_code()
            item.save(update_fields=["item_code"])
        item_code = item.item_code
        item_barcode = generate_barcode(item.item_code)
        item_label = f"{item.name} {item.purity} - {item.item_code}"

    return render(request, 'print_customer.html', {
        'customer': customer,
        'item': item,
        'item_code': item_code,
        'item_barcode': item_barcode,
        'item_label': item_label,
    })



# Edit view
@login_required
def edit_item(request, item_id):
    item = get_object_or_404(JewelleryItem, id=item_id)
    if request.method == 'POST':
        form = JewelleryItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('add_item')  # ya koi aur appropriate redirect
    else:
        form = JewelleryItemForm(instance=item)
    return render(request, 'edit_item.html', {'form': form, 'item': item})


@csrf_exempt
def delete_item_ajax(request, item_id):
    if request.method == 'POST':
        try:
            item = JewelleryItem.objects.get(id=item_id)
            item.delete()
            return JsonResponse({'status': 'success'})
        except JewelleryItem.DoesNotExist:
            return JsonResponse({'status': 'not_found'}, status=404)
    return JsonResponse({'status': 'invalid'}, status=400)



from django.shortcuts import render
from .models import Customer

@login_required
def view_sales(request):
    customers = Customer.objects.all()
    return render(request, 'view_sales.html', {'customers': customers})




# Reports view
@login_required
def view_products(request):
    category_filter = request.GET.get('category')
    search_query = request.GET.get('search')

    print(f"Category filter received: {category_filter}")
    print(f"Search query received: {search_query}")

    items = JewelleryItem.objects.all()

    if category_filter and category_filter != 'All':
        items = items.filter(category=category_filter)

    if search_query:
        items = items.filter(name__icontains=search_query)

    print(f"Items count after filtering: {items.count()}")

    # Reports view
@login_required
def view_products(request):
    category_filter = request.GET.get('category')
    search_query = request.GET.get('search')

    print(f"Category filter received: {category_filter}")
    print(f"Search query received: {search_query}")

    items = JewelleryItem.objects.all()

    if category_filter and category_filter != 'All':
        items = items.filter(category=category_filter)

    if search_query:
        items = items.filter(name__icontains=search_query)

    print(f"Items count after filtering: {items.count()}")

    for item in items:
        print("ITEM:", item.name)
        print("CODE:", item.item_code)

        if item.item_code:
            item.barcode = generate_barcode(item.item_code)

    return render(request, 'view_products.html', {
        'items': items,
        'selected_category': category_filter or 'All',
        'search_query': search_query or '',
    })




# views.py
def print_sale(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id)
    return render(request, 'print_sale.html', {'sale': sale})

# views.py
# Example view for autocomplete results with full product data
from django.http import JsonResponse

def autocomplete_search(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')

    items = JewelleryItem.objects.all()

    if category and category != 'All':
        items = items.filter(category=category)

    if query:
        items = items.filter(name__icontains=query)

    # Return full product info with item code and barcode image
    results = []
    for item in items:
        if not item.item_code:
            item.item_code = item.generate_item_code()
            item.save(update_fields=["item_code"])

        results.append({
            'category': item.category,
            'name': item.name,
            'quantity': item.quantity,
            'purity': item.purity,
            'weight': item.weight,
            'item_code': item.item_code,
            'label': f"{item.name} {item.purity} - {item.item_code}",
            'barcode': generate_barcode(item.item_code),
        })

    return JsonResponse(results, safe=False)


@login_required
def edit_customer(request, id):

    customer = get_object_or_404(Customer, id=id)

    form = CustomerForm(request.POST or None, instance=customer)

    if form.is_valid():
        form.save()
        return redirect('add_customer')

    return render(request, 'edit_customer.html', {
        'form': form
    })


@login_required
def delete_customer(request, id):

    customer = get_object_or_404(Customer, id=id)

    customer.delete()

    return redirect('add_customer')


from .utils import generate_barcode

def jewellery_list(request):
    items = JewelleryItem.objects.all()

    for item in items:
        item.barcode = generate_barcode(item.item_code)

    return render(
        request,
        "jewellery_list.html",
        {"items": items}
    )