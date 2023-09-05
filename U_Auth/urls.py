from django.urls import path
from U_Auth.views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    
    path('login/', user_login, name='login'),
    path('register/', register, name='register'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('logout/', logout_view, name='logout'),
     path('accounts/password_change/', auth_views.PasswordChangeView.as_view(template_name='U_Auth/password_change.html'), name='password_change'),
    path('accounts/password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='U_Auth/password_change_done.html'), name='password_change_done'),
   
]



