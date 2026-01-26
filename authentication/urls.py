# authentication/urls.py
from django.urls import path
from . import views

app_name = 'authentication'  # ADD THIS LINE

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('switch-role/', views.switch_role_view, name='switch_role'),
]