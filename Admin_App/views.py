from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from Admin_App.models import *
from User_App.models import *
from U_Auth.models import User
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.db.models import Sum, F
# Create your views here.


@user_passes_test(lambda u: u.is_superuser, login_url='/U_Auth/admin_login/')
def dashboard(request):
    cart = Cart.objects.filter(ordered=True)
    cart_total = sum(x.total for x in cart)
    order_count = Order.objects.count()
    earnings = cart_total + order_count * 8
    user_count = User.objects.filter(is_customer=True).count()
    review_count =  Review.objects.count()
    product_count = Product.objects.count()
    

         
    context = {
        'order_count' : order_count,
        'earnings' : earnings,
        'user_count' : user_count,
        'product_count' : product_count,
        'review_count' : review_count

    }
    return render(request, 'Admin/dashboard.html', context)

@user_passes_test(lambda u: u.is_superuser, login_url='/U_Auth/admin_login/')
def product_list(request):
    products = Product.objects.all()
    return render(request, 'Admin/product_list.html', {'products': products})

@user_passes_test(lambda u: u.is_superuser, login_url='/U_Auth/admin_login/')
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'Admin/product_detail.html', {'product': product})

@user_passes_test(lambda u: u.is_superuser, login_url='/U_Auth/admin_login/')
def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        image = request.FILES.get('image')
        image_two = request.FILES.get('image_two')
        description = request.POST.get('description')
        actual_price = request.POST.get('actual_price')
        discount_price = request.POST.get('discount_price') or None

        try:
            product = Product.objects.create(name=name, image=image, image_two=image_two, description=description, actual_price=actual_price, discount_price=discount_price)
            return redirect('product_list')
        except ValidationError as e:
            error_message = str(e)
    else:
        error_message = None

    return render(request, 'Admin/add_product.html', {'error_message': error_message})

@user_passes_test(lambda u: u.is_superuser, login_url='/U_Auth/admin_login/')
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        name = request.POST.get('name')
        image = request.FILES.get('image')
        image_two = request.FILES.get('image_two')
        description = request.POST.get('description')
        actual_price = request.POST.get('actual_price')
        discount_price = request.POST.get('discount_price') or None

        product.name = name
        if image:
            product.image = image
        if image_two:
            product.image_two = image_two

        # Check if the user didn't select a new image and keep the previous one
        if not image and product.image:
            product.image = product.image

        # Similarly, check for image_two
        if not image_two and product.image_two:
            product.image_two = product.image_two


        product.description = description 
        product.actual_price = actual_price
        product.discount_price = discount_price
        product.save()
        
        messages.success(request,'success')
        return redirect('product_list')


    return render(request, 'Admin/edit_product.html', {'product': product})

@user_passes_test(lambda u: u.is_superuser, login_url='/U_Auth/admin_login/')
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect('product_list')
    
# @user_passes_test(lambda u: u.is_superuser, login_url='/U_Auth/admin_login/')
# def all_order(request):
#     current_page = 'all_order'
#     order = Order.objects.all().order_by('-id')
#     context = {
#         'current_page' : current_page,
#         'order' : order
#     }
#     return render(request, 'Admin/all_order.html', context)



@user_passes_test(lambda u: u.is_superuser, login_url='/U_Auth/admin_login/')
def all_order(request):
    current_page = 'all_order'
    
    # Retrieve all orders with the total amount for each order
    orders = Order.objects.annotate(total_amount=Sum('cart__total')).order_by('-id')

    # Add 8 to the total_amount for each order
    orders = orders.annotate(total_amount_with_8=F('total_amount') + 8).order_by('-id')

    context = {
        'current_page': current_page,
        'order': orders
    }
    return render(request, 'Admin/all_order.html', context)


@user_passes_test(lambda u: u.is_superuser, login_url='/U_Auth/admin_login/')
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

@user_passes_test(lambda u: u.is_superuser, login_url='/U_Auth/admin_login/') 
def order_view(request, order_id):
    order = Order.objects.get(id=order_id)

    subtotal = sum(x.total for x in order.cart.all())
    total_of_total = sum(x.total for x in order.cart.all()) + 8

    context = {
        'order' : order,
        'subtotal' : subtotal,
        'total_of_total' : total_of_total
    }
    return render(request, 'Admin/order_view.html', context)

@user_passes_test(lambda u: u.is_superuser, login_url='/U_Auth/admin_login/')
def customers(request):
    customers = User.objects.all().filter(is_superuser=False)
    context = {
        'customers' : customers
    }
    return render(request, 'Admin/customers.html', context)

@user_passes_test(lambda u: u.is_superuser, login_url='/U_Auth/admin_login/')
def enquiry(request):
    enquiry = Enquiry.objects.all()
    context = {
        'enquiry' : enquiry
    }
    return render(request, 'Admin/enquiry.html', context)


@user_passes_test(lambda u: u.is_superuser, login_url='/U_Auth/admin_login/')
def report(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    status = request.GET.get('status')

    # Retrieve all orders with the total amount for each order
    orders = Order.objects.annotate(total_amount=Sum('cart__total')).order_by('-id')

    # Apply filters based on user input
    if start_date:
        orders = orders.filter(date__gte=start_date)
    if end_date:
        orders = orders.filter(date__lte=end_date)
    if status:
        orders = orders.filter(status=status)

    # Add 8 to the total_amount for each order
    orders = orders.annotate(total_amount_with_8=F('total_amount') + 8).order_by('-id')

    context = {
        'orders': orders,
        'start_date': start_date,  # Pass the values to the context
        'end_date': end_date,
        'status': status,
    }
    return render(request, 'Admin/report.html', context)


