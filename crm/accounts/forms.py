from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
# Get the User Admin form
from django.contrib.auth.models import User
from django import forms
from .models import *

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user', 'first_name', 'last_name']


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__' # Create a list if u wanr a specific one like fileds = ['customer', ...etc]


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        # check the Doc. for these fields from this link:
        # https://docs.djangoproject.com/en/2.0/ref/contrib/auth/#django.contrib.auth.models.User.first_name
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']