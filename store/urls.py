from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('', views.product_list, name='product_list'),
    path('cart/add/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('cart/remove/<int:id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('password-reset/',
     auth_views.PasswordResetView.as_view(template_name='store/password_reset.html'),
     name='password_reset'),

path('password-reset/done/',
     auth_views.PasswordResetDoneView.as_view(template_name='store/password_reset_done.html'),
     name='password_reset_done'),

path('reset/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(template_name='store/password_reset_confirm.html'),
     name='password_reset_confirm'),

path('reset/done/',
     auth_views.PasswordResetCompleteView.as_view(template_name='store/password_reset_complete.html'),
     name='password_reset_complete'),
]
