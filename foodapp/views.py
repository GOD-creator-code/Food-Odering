from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm

from .models import Category, FoodItem, Order
from .forms import OrderForm

# Helper function: check if user is chef
def is_chef(user):
    return user.is_authenticated and user.groups.filter(name='chef').exists()

# Landing page at '/' - role based access
def home_or_login(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        if is_chef(request.user):
            return redirect('chef_orders')
        else:
            categories = Category.objects.all()
            return render(request, 'foodapp/categories.html', {'categories': categories})

# Login view with role-based redirect
def role_based_login(request):
    if request.user.is_authenticated:
        if is_chef(request.user):
            return redirect('chef_orders')
        else:
            return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if is_chef(user):
                return redirect('chef_orders')
            else:
                return redirect('home')
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = AuthenticationForm()

    return render(request, 'foodapp/login.html', {'form': form})

# Logout view
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

# Customer home page
@login_required
def home(request):
    categories = Category.objects.all()
    return render(request, 'foodapp/categories.html', {'categories': categories})

def place_order(request):
    food_id = request.GET.get('food_id')
    initial_data = {}
    if food_id:
        food = get_object_or_404(FoodItem, id=food_id)
        initial_data['food'] = food

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('order_success')
    else:
        form = OrderForm(initial=initial_data)

    return render(request, 'foodapp/order_form.html', {'form': form})

def order_success(request):
    return render(request, 'foodapp/order_success.html')

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'foodapp/categories.html', {'categories': categories})

def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    food_items = FoodItem.objects.filter(category=category)

    cart = request.session.get('cart', {})
    cart_item_count = sum(cart.values())

    return render(request, 'foodapp/category_detail.html', {
        'category': category,
        'food_items': food_items,
        'cart_item_count': cart_item_count,
    })

def add_to_cart(request, food_id):
    cart = request.session.get('cart', {})
    cart[str(food_id)] = cart.get(str(food_id), 0) + 1
    request.session['cart'] = cart
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def remove_from_cart(request, food_id):
    cart = request.session.get('cart', {})
    if str(food_id) in cart:
        del cart[str(food_id)]
        request.session['cart'] = cart
    return HttpResponseRedirect(reverse('cart'))

def change_quantity(request, food_id, action):
    cart = request.session.get('cart', {})
    if str(food_id) in cart:
        if action == 'increase':
            cart[str(food_id)] += 1
        elif action == 'decrease':
            cart[str(food_id)] -= 1
            if cart[str(food_id)] <= 0:
                del cart[str(food_id)]
        request.session['cart'] = cart
    return HttpResponseRedirect(reverse('cart'))

def cart_view(request):
    cart = request.session.get('cart', {})
    food_ids = cart.keys()
    food_items = FoodItem.objects.filter(id__in=food_ids)
    cart_items = []
    total = 0

    for food in food_items:
        quantity = cart.get(str(food.id), 0)
        subtotal = quantity * food.price
        total += subtotal
        cart_items.append({
            'food': food,
            'quantity': quantity,
            'subtotal': subtotal,
        })

    return render(request, 'foodapp/cart.html', {
        'cart_items': cart_items,
        'total': total,
    })

@login_required
def checkout_view(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "Your cart is empty!")
        return redirect('cart')

    if request.method == "POST":
        items = FoodItem.objects.filter(id__in=cart.keys())
        total_price = sum(item.price * cart[str(item.id)] for item in items)

        order = Order.objects.create(
            customer_name=request.user.get_full_name() or request.user.username,
            customer_phone=request.POST.get('phone'),
            total_price=total_price
        )
        order.items.set(items)
        order.save()

        request.session['cart'] = {}
        messages.success(request, "Order placed successfully!")
        return redirect('order_success')

    return render(request, 'foodapp/checkout.html')

@login_required
@user_passes_test(is_chef)
def chef_orders_view(request):
    orders = Order.objects.order_by('-ordered_at')

    return render(request, 'foodapp/chef_orders.html', {'orders': orders})

@login_required
@user_passes_test(is_chef)
def mark_order_ready(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.is_ready = True
    order.save()
    return redirect('chef_orders')

@login_required
@user_passes_test(is_chef)
def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    messages.success(request, "Order deleted successfully.")
    return redirect('chef_orders')
