from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list_view, name='list'),
    path('create/', views.product_create_view, name='create'),
    path('<int:pk>/edit/', views.product_update_view, name='update'),
    path('<int:pk>/delete/', views.product_delete_view, name='delete'),
    path('<int:pk>/toggle/', views.product_toggle_availability_view, name='toggle_availability'),
    path('<slug:slug>/', views.product_detail_view, name='detail'),
]
