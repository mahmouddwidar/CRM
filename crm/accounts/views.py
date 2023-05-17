from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import OrderForm, CreateUserForm, CustomerForm
from .filter import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import *
from django.contrib.auth.models import Group

# Create your views here.
@unauthenticated_user
def registerPage(request):

    # Importing The Sign up form from django
    form = CreateUserForm()

    if request.method == 'POST':
        # Pass the data into the form
        form = CreateUserForm(request.POST)
        # Validate the data
        if form.is_valid():
            user = form.save()
            # Get the name that the user just entered
            username = form.cleaned_data.get('username')

            # GEt the group named 'customer' and don't forget to import the Group model
            # group = Group.objects.get(name='customer')
            # Add the user into the group
            # user.groups.add(group)

            # Connect the user table to the customer table in my DB
            # اللى هو بقوله فى جدول الزبون اعمل او دخل فيه اللى يوزر اللى لسه معمول ف يبقى موجود عندى فى الجدولين كده
            # Customer.objects.create(user=user,)

            messages.success(request, 'Account was created for ' + username)
            return redirect('login')

    context = {'title': 'Register', 'form': form}
    return render(request, 'accounts/register.html', context)


@unauthenticated_user
def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR Password is incorrect!')

    context = {'title': 'Login'}
    return render(request, 'accounts/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@admin_only
def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()

    totat_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'customers': customers, 'orders': orders,
               'totat_orders': totat_orders, 'delivered': delivered,
               'pending': pending, 'title': 'CRM Home'}

    return render(request, 'accounts/dashboard.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    # Get the whole orders for this customer or this user
    orders = request.user.customer.order_set.all()

    # Count the numbers of orders from my query 'orders' not from the class Order like the home page
    totat_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    # Get The logged in user's ID by: 'request.user.id'
    first_name = request.user.first_name # To get the first name from the user's table
    last_name = request.user.last_name  # To get the last name from the user's table

    context = {'title': first_name.capitalize() + ' ' + last_name.capitalize(),
               'orders': orders,
               'totat_orders': totat_orders,
               'delivered': delivered,
               'pending': pending}
    return render(request, 'accounts/user.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST ,request.FILES ,instance=customer)
        if form.is_valid():
            form.save()

    user_name = request.user.customer.name # To get the first name from the user's table
    name = request.user.first_name
    context = {'title': name,
               'form': form}
    return render(request, 'accounts/account_settings.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()

    context = {'products': products, 'title': 'Produscts'}
    return render(request, 'accounts/products.html',context )



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, primary_key):
    customer = Customer.objects.get(id=primary_key)
    orders = customer.order_set.all()
    order_count = orders.count()
    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {'customer': customer, 'orders': orders, 'order_count': order_count, 'title': customer.name, 'myFilter': myFilter.form}
    return render(request, 'accounts/customer.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def create_order(request):
    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'title': 'Create order', 'form': form}
    return render(request, 'accounts/create_order.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def update_order(request, primary_key):
    order = Order.objects.get(id=primary_key)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'title': 'Update order', 'form': form}
    return render(request, 'accounts/create_order.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_order(request, primary_key):
    order = Order.objects.get(id=primary_key)
    context = {'title': 'Delete item', 'item': order}

    if request.method == 'POST':
        order.delete()
        return redirect('/')

    return render(request, 'accounts/delete.html', context)