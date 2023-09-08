from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from Admin_App.models import Product
from django.contrib import messages
from User_App.models import *
from django.http import JsonResponse
from django.db.models import Avg
from django.db.models import Sum, F

def home(request):
    current_page = 'home'
    products = Product.objects.all()

     # Calculate the total rating for each product
    for product in products:
        product.total_rating = Review.objects.filter(product=product).aggregate(Avg('rating'))['rating__avg']
    
    context = {
        'current_page': current_page,
        'products': products,  # Use 'products' instead of 'product'
        
    }
    return render(request, 'User/home.html', context)

@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    user = request.user

    cart, created = Cart.objects.get_or_create(
        user=user,
        product=product,
        ordered=False
    )

    if not created and not cart.ordered:
        # If cart item exists and is not ordered, increment the quantity
        cart.quantity += 1
        cart.save()
    messages.success(request, f"Cart added successfully.")
    return redirect("home")


@login_required
def cart_list(request):
    current_page = 'cart_list'
    user = request.user
    cart = Cart.objects.filter(user=user).order_by('-id')
    
    subtotal = sum(x.total for x in cart if not x.ordered)
    total_of_total = sum(x.total for x in cart if not x.ordered) + 8

    context = {
        'current_page': current_page,
        'cart' : cart,
        'subtotal' :subtotal,
        'total_of_total' : total_of_total
    }
    return render(request, 'User/cart_list.html', context)


@login_required
def increase_quantity(request, cart_id):
    cart = Cart.objects.get(id=cart_id)
    cart.quantity += 1
    cart.save()
    return redirect('cart_list')

@login_required
def decrease_quantity(request, cart_id):
    cart = Cart.objects.get(id=cart_id)
    if cart.quantity > 1: # make sure the quantity doesn't go below 1.
        cart.quantity -= 1  
        cart.save()
    return redirect('cart_list')


def delete_cart(request, cart_id):
    cart = Cart.objects.get(id=cart_id)
    cart.delete()
    return redirect('cart_list')


def product_view(request, product_id):
    current_page = 'product_view'
    product = Product.objects.get(id=product_id)
    review = Review.objects.filter(product=product)
    
    
    existing_review = None  # Initialize existing_review to None
    if request.user.is_authenticated:
        existing_review = Review.objects.filter(user=request.user, product=product).first()


    # Calculate the total rating for the product
    total_rating = review.aggregate(Avg('rating'))['rating__avg']
      
    context = {
        'current_page': current_page,
        'product' : product,
        'existing_review' : existing_review,
        'review' : review,
        'total_rating': total_rating,  # Add total_rating to the context
    }
    return render(request, 'User/product_view.html', context)



# def product_view(request, product_id):
#     current_page = 'product_view'
#     product = Product.objects.get(id=product_id)
#     reviews = Review.objects.filter(product=product)

#     existing_review = None  # Initialize existing_review to None
#     if request.user.is_authenticated:
#         existing_review = Review.objects.filter(user=request.user, product=product).first()

#     # Calculate the total rating for the product
#     total_rating = reviews.aggregate(Avg('rating'))['rating__avg']

#     context = {
#         'current_page': current_page,
#         'product': product,
#         'existing_review': existing_review,
#         'review': reviews,
#         'total_rating': total_rating,  # Add total_rating to the context
#     }
#     return render(request, 'User/product_view.html', context)


@login_required
def add_to_cart_two(request, product_id):
    product = Product.objects.get(id=product_id)
    user = request.user

    cart, created = Cart.objects.get_or_create(
        user=user,
        product=product,
        ordered=False
    )

    if not created and not cart.ordered:
        # If cart item exists and is not ordered, increment the quantity
        cart.quantity += 1
        cart.save()
    messages.success(request, f"Cart added successfully.")
    return redirect("product_view" , product_id=product.id)

@login_required
def order(request):
    cart = Cart.objects.filter(user=request.user, ordered=False).order_by('-id')

    subtotal = sum(x.total for x in cart)
    total_of_total = sum(x.total for x in cart if not x.ordered) + 8

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        city = request.POST.get('city')
        postel_code = request.POST.get('postel_code')
        phone = request.POST.get('phone')

        order = Order.objects.create(
            user=request.user,
            first_name=first_name,
            last_name=last_name,
            address=address,
            city=city,
            postel_code=postel_code,
            phone=phone,
        )
        order.cart.set(cart)  # For adding cart items assosiated with user (its manytomanyfield thats way using this)

        for field in cart:
            field.ordered = True
            field.save()
        messages.success(request, f"Order added successfully.")
        return redirect('home')
    
    context = {
        'cart' : cart,
        'subtotal' : subtotal,
        'total_of_total' : total_of_total
    }

    return render(request, 'User/order.html', context)

def about(request):
    return render(request, 'User/about.html')

def blog(request):
    return render(request, 'User/blog.html')



def search_results(request):
    search_query = request.GET.get('q')
    products = Product.objects.filter(name__icontains=search_query)

    context = {
        'search_query': search_query,
        'product': products,
    }
    return render(request, 'User/search_results.html', context)  # Use 'search.html' template

def search_suggestions(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(name__icontains=query)[:5]  # Limit suggestions to 5
        suggestions = [product.name for product in products]
        return JsonResponse(suggestions, safe=False)
    return JsonResponse([], safe=False)





def shop(request):
    current_page = 'shop'
    products = Product.objects.all()

    context = {
        'current_page': current_page,
        'products': products,  # Use 'products' instead of 'product'
        
    }
    return render(request, 'User/shop.html', context)


@login_required
def add_to_cart_three(request, product_id):
    product = Product.objects.get(id=product_id)
    user = request.user

    cart, created = Cart.objects.get_or_create(
        user=user,
        product=product,
        ordered=False
    )

    if not created and not cart.ordered:
        # If cart item exists and is not ordered, increment the quantity
        cart.quantity += 1
        cart.save()
    messages.success(request, f"Cart added successfully.")
    return redirect("shop")

@login_required
def profile(request):
    user = request.user
    context = {
        'user' : user,
    }
    return render(request, 'User/profile.html' , context)



# @login_required
# def order_list(request):
#     current_page = 'order_list'
#     user = request.user
#     order = Order.objects.filter(user=user).order_by('-id')
    
#     context = {
#         'current_page': current_page,
#         'order' : order,
        
#     }
#     return render(request, 'User/order_list.html', context)




@login_required
def order_list(request):
    current_page = 'order_list'
    user = request.user

    # Retrieve all orders with the total amount for each order
    orders = Order.objects.filter(user=user).annotate(total_amount=Sum('cart__total')).order_by('-id')

    # Add 8 to the total_amount for each order
    orders = orders.annotate(total_amount_with_8=F('total_amount') + 8).order_by('-id')

    context = {
        'current_page': current_page,
        'order': orders
    }
    return render(request, 'User/order_list.html', context)


@login_required
def add_review(request, product_id):
    user = request.user
    product = Product.objects.get(id=product_id)

    if request.method == 'POST':
        rating = request.POST.get('rating')
        head = request.POST.get('head')
        comment = request.POST.get('comment')
        review = Review.objects.create(
            user=user,
            product=product,
            rating=rating,
            head=head,
            comment=comment
        )
        return redirect('product_view', product_id=product.id)
    return render(request, 'User/add_review.html')


@login_required
def edit_review(request, product_id, existing_review_id):
    product = Product.objects.get(id=product_id)
    existing_review = Review.objects.get(id=existing_review_id)
    
    if request.method == 'POST':
        existing_review.rating = request.POST.get('rating')
        existing_review.head = request.POST.get('head')
        existing_review.comment = request.POST.get('comment')
        existing_review.save()
        return redirect('product_view', product_id=product.id)
    
    context = {
        'existing_review' : existing_review
    }
    return render(request, 'User/edit_review.html', context)

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        enquiry = Enquiry.objects.create(
            name=name,
            email=email,
            message=message,
        )
        messages.success(request, 'thankyou for your ')
    return render(request, 'User/contact.html')


