from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class UserRegistrationForm(UserCreationForm):
    """
    Form for user registration
    """
    USER_TYPE_CHOICES = [
        ('customer', 'Customer'),
        ('seller', 'Seller'),
    ]
    
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, widget=forms.RadioSelect, initial='customer')
    email = forms.EmailField(required=True)
    
    # Seller specific fields
    business_name = forms.CharField(required=False)
    phone = forms.CharField(required=False)
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    city = forms.CharField(required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
    def clean(self):
        cleaned_data = super().clean()
        user_type = cleaned_data.get('user_type')
        
        if user_type == 'seller':
            if not cleaned_data.get('business_name'):
                self.add_error('business_name', 'Business Name is required for sellers.')
            if not cleaned_data.get('phone'):
                self.add_error('phone', 'Phone number is required for sellers.')
            if not cleaned_data.get('address'):
                self.add_error('address', 'Address is required for sellers.')
            if not cleaned_data.get('city'):
                self.add_error('city', 'City is required for sellers.')
                
        return cleaned_data


class UserLoginForm(AuthenticationForm):
    """
    Form for user login
    """
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
