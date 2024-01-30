from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse

from .models import *
from .utils import cookieCart, cartData, guestOrder
from .forms import RegistrationForm, ProductForm

import json
import datetime


def store(request):
    data = cartData(request)
    cartItems = data['cartItems']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)


def product_detail(request, product_id):
    data = cartData(request)
    cartItems = data['cartItems']

    product = get_object_or_404(Product, pk=product_id)
    context = {'product': product, 'cartItems': cartItems}
    return render(request, 'store/product_detail.html', context)


def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)


def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('ProductId: ', productId)
    print('Action: ', action)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    elif action == 'delete':
        orderItem.quantity = 0

    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id
    cart_total = float(order.get_cart_total)

    if total == cart_total:
        order.complete = True
    order.save()

    ShippingAddress.objects.create(
        customer=customer,
        order=order,
        street_name=data['shipping']['street_name'],
        street_number=data['shipping']['street_number'],
        city=data['shipping']['city'],
        country=data['shipping']['country'],
        zipcode=data['shipping']['zipcode']
    )

    return JsonResponse('Payment complete!', safe=False)


User


def userLogin(request):
    data = cartData(request)
    cartItems = data['cartItems']

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('store')
        else:
            error_message = 'Invalid username or password.'
            return render(request, 'store/login.html', {'error_message': error_message})
    context = {'cartItems': cartItems}
    return render(request, 'store/login.html', context)


def userLogout(request):
    logout(request)
    return redirect('store')


def userRegistration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Customer.objects.create(user=user)
            login(request, user)
            return redirect('store')
    else:
        form = RegistrationForm()
    return render(request, 'store/registration.html', {'form': form})


@user_passes_test(lambda user: user.is_superuser)
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('store')
    else:
        form = ProductForm()

    return render(request, 'store/add_product.html', {'form': form})


def delete_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    # Check if the user is a superuser before allowing deletion
    if request.user.is_superuser:
        product.delete()

    return redirect('store')