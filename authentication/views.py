from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm


def login_view(request):
    """
    Handle user login
    """
    print("=" * 60)
    print("LOGIN VIEW CALLED")
    print(f"Method: {request.method}")
    print(f"User authenticated: {request.user.is_authenticated}")
    
    if request.user.is_authenticated:
        print("User already authenticated, redirecting to /")
        return redirect('/')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        print(f"Username from POST: '{username}'")
        print(f"Password from POST: '{password}'")
        
        user = authenticate(request, username=username, password=password)
        
        print(f"Authentication result: {user}")
        
        if user is not None:
            print(f"User authenticated successfully: {user.username}")
            login(request, user)
            print("User logged in via Django login()")
            messages.success(request, f'Welcome back, {username}!')
            
            try:
                if hasattr(user, 'seller_profile'):
                    print("User is a seller, redirecting to sellers:profile")
                    return redirect('sellers:profile')
            except Exception as e:
                print(f"Seller check error: {e}")
            
            next_url = request.GET.get('next', '/')
            print(f"Redirecting to: {next_url}")
            return redirect(next_url)
        else:
            print("Authentication FAILED - Invalid credentials")
            messages.error(request, 'Invalid username or password. Please try again.')
    
    print("Rendering login.html template")
    print("=" * 60)
    return render(request, 'authentication/login.html')

def register_view(request):
    """
    Handle user registration
    """
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created successfully for {username}! You can now log in.')
            return redirect('authentication:login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'authentication/register.html', {'form': form})


@login_required
def logout_view(request):
    """
    Handle user logout
    """
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('/')


def forgot_password_view(request):
    """
    Handle forgot password
    """
    return render(request,'authentication/forgot_password.html')