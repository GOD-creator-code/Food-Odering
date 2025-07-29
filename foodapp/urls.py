from django.urls import path
from . import views

urlpatterns = [
    # Landing and auth
    path('', views.home_or_login, name='home_or_login'),  # "/" → redirects based on role
    path('login/', views.role_based_login, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Customer dashboard
    path('home/', views.home, name='home'),  # shows categories

    # Chef dashboard
    path('chef/orders/', views.chef_orders_view, name='chef_orders'),
    path('order/<int:order_id>/ready/', views.mark_order_ready, name='mark_order_ready'),
    path('order/<int:order_id>/delete/', views.delete_order, name='delete_order'),

    # Ordering
    path('place_order/', views.place_order, name='place_order'),
    path('order_success/', views.order_success, name='order_success'),

    # Categories & Food Items
    path('categories/', views.category_list, name='category_list'),  # view all categories
    path('category/<int:category_id>/', views.category_detail, name='category_detail'),

    # Cart
    path('add_to_cart/<int:food_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:food_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('change_quantity/<int:food_id>/<str:action>/', views.change_quantity, name='change_quantity'),
    path('cart/', views.cart_view, name='cart'),
    path('checkout/', views.checkout_view, name='checkout'),
]
