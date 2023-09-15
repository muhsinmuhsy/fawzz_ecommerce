from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from U_Auth.models import  User
from django.contrib import messages
from django.contrib.auth import logout


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        email = request.POST.get('email')
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')
        
        if password == confirm_password:
            # Check if the username is already taken
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists.')
                return redirect('register')

            # Create the user
            user = User.objects.create_user(
                username=username, 
                password=password,
                first_name=first_name, 
                last_name=last_name,
                address=address,
                email=email,
                mobile=mobile,
                is_customer = True
                )
            user.save()
            
            # Log the user in after registration
            user = authenticate(request, username=username, password=password)
            login(request, user)
            
            messages.success(request, 'Registered Successfully and logged in.')
            return redirect('home')
        else:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')

    return render(request, 'U_Auth/register.html')



def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'Username does not exist.')
            return render(request, 'U_Auth/login.html')

        if user.check_password(password):
            authenticated_user = authenticate(request, username=username, password=password)
            if authenticated_user is not None:
                login(request, authenticated_user)
                messages.success(request, 'Login Successfully')
                return redirect('home')
            else:
                messages.error(request, 'Invalid login credentials.')
        else:
            messages.error(request, 'Incorrect password.')

        return render(request, 'U_Auth/login.html')

    return render(request, 'U_Auth/login.html')





def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        
        # Update the user's profile information
        user.first_name = first_name
        user.last_name = last_name
        user.address = address  # Assuming you have a UserProfile model with an 'address' field
        user.mobile = mobile  # Assuming you have a UserProfile model with a 'mobile' field
        user.email = email 
        user.save()

        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')  # Redirect to the user's profile page after editing

    user = request.user
    context = {
        'user': user,
    }
    return render(request, 'U_Auth/edit_profile.html', context)

def logout_view(request):
    logout(request)
    return redirect('home')



def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            error = 'User Name or Password Incorrect.'
    else:
        error = None
    return render(request, 'U_Auth/admin_login.html', {'error': error})

