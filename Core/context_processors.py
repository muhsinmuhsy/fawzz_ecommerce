def context(request):
    # Your logic to generate data goes here
    from User_App.models import Cart
    try:
        cart_items = Cart.objects.filter(user=request.user,ordered=False).count()
    except:
        cart_items = 0
    data = {
        'cart_items_count' : cart_items
    }
    return data