def context(request):
    # Your logic to generate data goes here
    from User_App.models import Cart
    cart_items = Cart.objects.filter(user=request.user,ordered=False)
    data = {
        'cart_items_count' : cart_items.count()
    }
    return data