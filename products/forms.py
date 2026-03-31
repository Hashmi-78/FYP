from django import forms
from django.db import IntegrityError, transaction
from django.utils.text import slugify

from .models import Category, Product


class NegotiationOfferForm(forms.Form):
    offer = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0,
        widget=forms.NumberInput(
            attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-600 outline-none',
                'placeholder': 'Enter your offer',
                'step': '0.01',
            }
        ),
    )

class ProductForm(forms.ModelForm):
    new_category = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-600 outline-none',
                'placeholder': 'Or type a new category name',
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'category' in self.fields:
            self.fields['category'].queryset = Category.objects.filter(is_active=True)

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

    def save(self, commit=True):
        instance = super().save(commit=False)

        new_category_name = (self.cleaned_data.get('new_category') or '').strip()
        if new_category_name:
            existing = Category.objects.filter(name__iexact=new_category_name).first()
            if existing:
                instance.category = existing
            else:
                base_slug = slugify(new_category_name) or 'category'
                slug = base_slug
                i = 2
                while Category.objects.filter(slug=slug).exists():
                    slug = f"{base_slug}-{i}"
                    i += 1

                try:
                    with transaction.atomic():
                        instance.category = Category.objects.create(
                            name=new_category_name,
                            slug=slug,
                            is_active=True,
                        )
                except IntegrityError:
                    instance.category = Category.objects.filter(name__iexact=new_category_name).first()

        if commit:
            instance.save()
            self.save_m2m()
        return instance

