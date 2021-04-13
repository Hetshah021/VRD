# accounts/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import MyUser

class MyUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = MyUser
        fields = ('first_name', 'last_name', 'email', 'username', 'password', 'mobile_number', 'birth_date')

class MyUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm):
        model = MyUser
        fields = ('first_name', 'last_name', 'email', 'username', 'password', 'mobile_number', 'birth_date')

class RegisterForm(forms.ModelForm):
    class Meta(forms.ModelForm):
        model = MyUser
        fields = ['first_name', 'last_name', 'email', 'username', 'mobile_number', 'birth_date']
        widgets = {
            'birth_date': forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD'})
        }

class ChangePasswordForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = MyUser
        fields = ['username', 'password']
        # excludes = ['first_name', 'last_name']
        label = {
            'password': 'Password'
        }

    def save(self):
        password = self.cleaned_data.pop('password')
        u = super().save()
        u.set_password(password)
        u.save()
        return u

