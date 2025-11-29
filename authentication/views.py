from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
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
    print("=" * 60)
    print("REGISTER VIEW CALLED")
    print(f"Method: {request.method}")
    print(f"User: {request.user}")
    print(f"Is authenticated: {request.user.is_authenticated}")

    if request.user.is_authenticated:
        print("User already authenticated, redirecting to /")
        return redirect('/')
    
    if request.method == 'POST':
        print("Processing POST request")
        print(f"POST data keys: {request.POST.keys()}")
        print(f"POST data: {dict(request.POST)}")
        
        form = UserRegistrationForm(request.POST)
        print(f"Form created: {form}")
        print(f"Form data: {form.data}")
        
        print("Checking form validity...")
        is_valid = form.is_valid()
        print(f"Form is_valid result: {is_valid}")
        
        if is_valid:
            print("Form is valid. Saving user...")
            print(f"Cleaned data: {form.cleaned_data}")
            try:
                print("Calling form.save()...")
                user = form.save()
                print(f"User saved successfully!")
                print(f"  - Username: {user.username}")
                print(f"  - ID: {user.id}")
                print(f"  - Email: {user.email}")
                print(f"  - Is active: {user.is_active}")
                
                username = form.cleaned_data.get('username')
                messages.success(request, f'Account created successfully for {username}! You can now log in.')
                print("Success message added")
                print("Redirecting to authentication:login")
                return redirect('authentication:login')
            except Exception as e:
                print(f"ERROR SAVING USER: {type(e).__name__}: {e}")
                import traceback
                print(f"Traceback: {traceback.format_exc()}")
                messages.error(request, f"Error creating account: {e}")
        else:
            print("FORM IS INVALID")
            print(f"Form errors: {form.errors}")
            print(f"Form errors as dict: {dict(form.errors)}")
            for field, errors in form.errors.items():
                print(f"  Field '{field}': {errors}")
            messages.error(request, 'Please correct the errors below.')
    else:
        print("Processing GET request - showing empty form")
        form = UserRegistrationForm()
        print(f"Empty form created: {form}")
    
    print(f"Rendering register.html with form: {form}")
    print("=" * 60)
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
    if request.method == 'POST':
        email = request.POST.get('email')
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            opts = {
                'use_https': request.is_secure(),
                'token_generator': default_token_generator,
                'from_email': None,
                'email_template_name': 'registration/password_reset_email.html',
                'request': request,
            }
            form.save(**opts)
            messages.success(request, 'We have emailed you instructions for setting your password, if an account exists with the email you entered.')
            return redirect('authentication:login')
        else:
            messages.error(request, 'Please enter a valid email address.')
            
    return render(request, 'authentication/forgot_password.html')