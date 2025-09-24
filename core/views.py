from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .forms import CustomerForm, LoginForm, SignupForm
from .models import Item, Cart, Order
from django.db.models import Q
from django.contrib.auth import get_user_model

User = get_user_model()


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)  # Ensure backend supports email auth
            if user is not None:
                auth_login(request, user)
                messages.success(request, f'Welcome back, {user.name}!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid email or password.')
    else:
        form = LoginForm()
    return render(request, 'core/login.html', {'form': form})


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already registered. Please login or use another email.')
                # You can prefill the form with previous data, no need to call signup_view recursively
                return render(request, 'core/signup.html', {'form': form})
            
            # Create user with create_user (handles password hashing)
            user = User.objects.create_user(
                name=form.cleaned_data['name'],
                email=email,
                password=form.cleaned_data['password'],
                city=form.cleaned_data['city']
            )
            messages.success(request, 'Account created successfully! Please login.')
            return redirect('login')
    else:
        form = SignupForm(initial={'name': 'Nandini', 'email': 'nandiniverma@gmail.com', 'password': '12345678', 'city': 'Ujjain'})
    return render(request, 'core/signup.html', {'form': form})


def home(request):
    name = request.user.name if request.user.is_authenticated else 'Guest'
    return render(request, 'core/home.html', {'name': name})


@login_required(login_url='login')
def logout(request):
    auth_logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('login')


def about(request):
    return render(request, 'core/about.html')


def help(request):
    return render(request, 'core/help.html')


def food(request):
    name = request.user.name if request.user.is_authenticated else 'Guest'
    query = request.GET.get('q')
    category = request.GET.get('category')
    dishes = Item.objects.all()
    if category:
        dishes = dishes.filter(category=category)
    if query:
        dishes = dishes.filter(name__icontains=query)
    categories = Item.objects.values_list('category', flat=True).distinct()
    return render(request, 'core/food.html', {
        'name': name,
        'dishes': dishes,
        'categories': categories,
        'selected_category': category
    })


@login_required(login_url='login')
def add_to_cart(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, item=item)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f"{item.name} added to cart.")
    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required(login_url='login')
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.get_total_price() for item in cart_items)
    return render(request, 'core/cart.html', {'cart_items': cart_items, 'total': total, 'name': request.user.name})


@login_required(login_url='login')
def customer_details_view(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            request.session['customer_data'] = form.cleaned_data
            return redirect('order_summary')
    else:
        form = CustomerForm()
    return render(request, 'core/customer_details.html', {'form': form, 'name': request.user.name})


@login_required(login_url='login')
def order_summary_view(request):
    customer_data = request.session.get('customer_data')
    if not customer_data:
        return redirect('customer_details')

    user = request.user
    cart_items = Cart.objects.filter(user=user)
    total = sum(item.get_total_price() for item in cart_items)
    item_summary = "\n".join([f"{item.item.name} x{item.quantity}" for item in cart_items])

    order = Order.objects.create(
        user=user,
        customer_name=customer_data['name'],
        address=f"{customer_data['address']}, {customer_data['city']} - {customer_data['pincode']}",
        phone=customer_data['phone'],
        items=item_summary,
        total=total,
        status='Preparing'
    )

    messages.success(request, f'Order Placed Successfully, {user.name}!')
    return render(request, 'core/order_summary.html', {
        'data': customer_data,
        'order': order,
        'cart_items': cart_items,
        'total': total,
        'name': user.name
    })


@login_required(login_url='login')
def track_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'core/order_tracking.html', {'orders': orders})


def menu(request):
    dishes = Item.objects.all()
    return render(request, 'menu.html', {'dishes': dishes})


@login_required(login_url='login')
def placeorder(request):
    return render(request, 'core/placeorder.html', {'name': request.user.name})


def search_view(request):
    query = request.GET.get('q')
    if query:
        results = Item.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    else:
        results = Item.objects.all()[:10]
    return render(request, 'search_results.html', {'query': query, 'results': results})


@login_required(login_url='login')
def delete_cart_item(request, item_id):
    if request.method == "POST":
        cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
        cart_item.delete()
    return redirect('view_cart')


@login_required(login_url='login')
def increase_quantity(request, cart_item_id):
    cart_item = get_object_or_404(Cart, pk=cart_item_id, user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('view_cart')


@login_required(login_url='login')
def decrease_quantity(request, cart_item_id):
    cart_item = get_object_or_404(Cart, pk=cart_item_id, user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('view_cart')


def feedback(request):
    return render(request, 'core/feedback.html')
