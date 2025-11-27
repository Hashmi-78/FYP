from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'stock', 'main_image']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-600 outline-none',
                'placeholder': 'Enter product name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-600 outline-none',
                'placeholder': 'Describe your product',
                'rows': 4
            }),
            'price': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-600 outline-none',
                'placeholder': '0.00',
                'step': '0.01'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-600 outline-none'
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-600 outline-none',
                'placeholder': '0',
                'min': '0'
            }),
            'main_image': forms.FileInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-600 outline-none',
                'accept': 'image/*'
            })
        }

