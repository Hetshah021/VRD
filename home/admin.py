# users/admin.py
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import MyUserCreationForm, MyUserChangeForm
from .models import MyUser, CameraDetails, VehicleDetails

class MyUserAdmin(UserAdmin):
    add_form = MyUserCreationForm
    form = MyUserChangeForm
    model = MyUser
    list_display = ['first_name', 'last_name', 'email', 'username', 'mobile_number', 'birth_date']
    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ('mobile_number', 'birth_date')}),
    ) #this will allow to change these fields in admin module


admin.site.register(MyUser, MyUserAdmin)
admin.site.register(CameraDetails)
admin.site.register(VehicleDetails)