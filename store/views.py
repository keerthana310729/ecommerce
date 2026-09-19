from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Product, Order


def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {
        'products': products
    })


def product_detail(request, id):
    product = Product.objects.get(id=id)
    return render(request, 'store/product_detail.html', {
        'product': product
    })


def add_to_cart(request, id):
    product = Product.objects.get(id=id)

    cart = request.session.get('cart', {})

    cart[str(id)] = cart.get(str(id), 0) + 1

    request.session['cart'] = cart

    return redirect('product_list')


def cart(request):
    cart = request.session.get('cart', {})
    products = []
    total = 0

    for id, quantity in cart.items():
        product = Product.objects.get(id=id)

        item_total = product.price * quantity
        total += item_total

        products.append({
            'product': product,
            'quantity': quantity,
            'item_total': item_total
        })

    return render(request, 'store/cart.html', {
        'products': products,
        'total': total
    })


def remove_from_cart(request, id):
    cart = request.session.get('cart', {})

    if str(id) in cart:
        cart[str(id)] -= 1

        if cart[str(id)] <= 0:
            del cart[str(id)]

    request.session['cart'] = cart

    return redirect('cart')


def checkout(request):
    if not request.user.is_authenticated:
        return redirect('login')

    cart = request.session.get('cart', {})
    products = []
    total = 0

    # Do not allow checkout if the cart is empty
    if not cart:
        return redirect('cart')

    for id, quantity in cart.items():
        product = Product.objects.get(id=id)

        item_total = product.price * quantity
        total += item_total

        products.append({
            'product': product,
            'quantity': quantity,
            'item_total': item_total
        })

    if request.method == 'POST':
        customer_name = request.POST['customer_name']
        email = request.POST['email']
        address = request.POST['address']
        payment_method = request.POST['payment_method']

        Order.objects.create(
            user=request.user,
            customer_name=customer_name,
            email=email,
            address=address,
            payment_method=payment_method,
            total=total
        )

        request.session['cart'] = {}

        return render(request, 'store/order_success.html')

    return render(request, 'store/checkout.html', {
        'products': products,
        'total': total
    })


@never_cache
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        from django.contrib.auth.models import User

        if User.objects.filter(username=username).exists():
            return render(request, 'store/register.html', {
                'error': 'Username already exists. Please choose another username.'
            })

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return redirect('login')

    return render(request, 'store/register.html')


@never_cache
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('product_list')

        else:
            return render(request, 'store/login.html', {
                'error': 'Invalid username or password.'
            })

    return render(request, 'store/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required(login_url='/login/')
def my_orders(request):
    orders = Order.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(request, 'store/my_orders.html', {
        'orders': orders
    })