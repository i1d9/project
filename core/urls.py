from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.search, name='search'),
    path('post/<str:pk>', views.post_profile, name='post-profile'),
    path('signup', views.signup, name='signup'),
    path('login', views.signin, name='signin'),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('upload', views.upload, name='upload'),
    path('logout', views.signout, name='logout'),
    path('settings', views.settings, name='settings'),
    path('order-summary', views.order_summary, name='order-summary'),
    path('checkout', views.checkout, name='checkout'),
    path('add-to-cart/<pk>/', views.add_to_cart, name='add-to-cart'),
    path('confirm-order/<int:pk>/', views.confirm_order, name='confirm-order'),
    path('remove-from-cart/<pk>/', views.remove_from_cart, name='remove-from-cart'),
    path('reduce-quantity-item/<pk>/', views.reduce_quantity_item, name='reduce-quantity-item'),
    path('my-orders', views.my_orders, name='my-orders'),
    path('customer-orders', views.customer_orders, name='customer-orders'),
    path('post/<str:post_id>/<int:rating>/', views.rate),
    path('delete/<pk>',views.delete_post,name='delete'),
    path('users',views.users, name='users'),
    path('transactions',views.transactions, name='transactions')
]