from django.urls import path
from . import views

app_name = 'sellers'

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('orders/', views.orders_view, name='orders'),
    path('profile/', views.profile_view, name='profile'),
    path('add-product/', views.add_product_view, name='add_product'),
    path('edit-product/<int:pk>/', views.edit_product_view, name='edit_product'),
    path('bulk-delete/', views.bulk_delete_products_view, name='bulk_delete_products'),
    path('messages/', views.messages_view, name='messages'),
    path('delivery/', views.delivery_view, name='delivery'),
    path('sales-graph/', views.sales_graph_view, name='sales_graph'),
    path('payment/', views.payment_view, name='payment'),
]

