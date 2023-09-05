from django.contrib import admin
from U_Auth.models import User 

# Register your models here.
@admin.register(User)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'username', 'is_superuser', 'is_customer' ]