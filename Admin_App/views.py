from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth.decorators import login_required
from Admin_App.models import *
from User_App.models import *
from U_Auth.models import User
from django.core.exceptions import ValidationError
# Create your views here.


@login_required(login_url='/U_Auth/admin_login/')
def dashboard(request):
    return render(request, 'Admin/dashboard.html')


def product_list(request):
    products = Product.objects.all()
    return render(request, 'Admin/product_list.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'Admin/product_detail.html', {'product': product})

def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        image = request.FILES.get('image')
        description = request.POST.get('description')
        actual_price = request.POST.get('actual_price')
        discount_price = request.POST.get('discount_price')

        try:
            product = Product.objects.create(name=name, image=image, description=description, actual_price=actual_price, discount_price=discount_price)
            return redirect('product_list')
        except ValidationError as e:
            error_message = str(e)
    else:
        error_message = None

    return render(request, 'Admin/add_product.html', {'error_message': error_message})

def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        name = request.POST.get('name')
        image = request.FILES.get('image')
        description = request.FILES.get('description')
        actual_price = request.POST.get('actual_price')
        discount_price = request.POST.get('discount_price')

        try:
            product.name = name
            if image:
                product.image = image
            product.description= description
            product.actual_price = actual_price
            product.discount_price = discount_price
            product.save()
            return redirect('product_list')
        except ValidationError as e:
            error_message = str(e)
    else:
        error_message = None

    return render(request, 'Admin/edit_product.html', {'product': product, 'error_message': error_message})

def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect('product_list')
    

def all_order(request):
    current_page = 'all_order'
    order = Order.objects.all().order_by('-id')
    context = {
        'current_page' : current_page,
        'order' : order
    }
    return render(request, 'Admin/all_order.html', context)

def order_update(request, order_id):
    order = Order.objects.get(id=order_id)
    if request.method == 'POST':
        status = request.POST.get('status')
        delivery_espected = request.POST.get('delivery_espected')

        if status and status in dict(order.STATUS): # for models STATUS choice
            order.status = status

        order.delivery_espected = delivery_espected

        order.save()
    return redirect('all_order')
    
def order_view(request, order_id):
    order = Order.objects.get(id=order_id)

    subtotal = sum(x.total for x in order.cart.all())
    total_of_total = sum(x.total for x in order.cart.all()) + 1

    context = {
        'order' : order,
        'subtotal' : subtotal,
        'total_of_total' : total_of_total
    }
    return render(request, 'Admin/order_view.html', context)


def customers(request):
    customers = User.objects.all().filter(is_superuser=False)
    context = {
        'customers' : customers
    }
    return render(request, 'Admin/customers.html', context)

def enquiry(request):
    enquiry = Enquiry.objects.all()
    context = {
        'enquiry' : enquiry
    }
    return render(request, 'Admin/enquiry.html', context)

