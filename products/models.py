from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Category(models.Model):
    """
    Product category model
    """
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Product model for all products in the store
    """
    name = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    
    # Pricing
    price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    discount_percentage = models.IntegerField(default=0, help_text='Discount percentage (0-100)')
    
    # Inventory
    stock = models.IntegerField(default=0)
    is_available = models.BooleanField(default=True)
    
    # Product details
    brand = models.CharField(max_length=200, blank=True)
    sku = models.CharField(max_length=100, unique=True, blank=True)
    
    # Images
    main_image = models.ImageField(upload_to='products/')
    image_2 = models.ImageField(upload_to='products/', blank=True, null=True)
    image_3 = models.ImageField(upload_to='products/', blank=True, null=True)
    image_4 = models.ImageField(upload_to='products/', blank=True, null=True)
    
    # Ratings and reviews
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    num_reviews = models.IntegerField(default=0)
    
    # AI features
    ai_recommended = models.BooleanField(default=False, help_text='AI recommended product')
    is_trending = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    
    # Seller
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['category', '-created_at']),
            models.Index(fields=['-rating']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if not self.sku:
            self.sku = f'PRD-{self.id or ""}-{slugify(self.name)[:20]}'
        super().save(*args, **kwargs)
    
    def get_discount_price(self):
        """Calculate discounted price"""
        if self.discount_percentage > 0:
            discount_amount = (self.price * self.discount_percentage) / 100
            return self.price - discount_amount
        return self.price
    
    def __str__(self):
        return self.name


class ProductReview(models.Model):
    """
    Product review model
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    title = models.CharField(max_length=200)
    comment = models.TextField()
    is_verified_purchase = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['product', 'user']
    
    def __str__(self):
        return f'{self.user.username} - {self.product.name} ({self.rating}★)'
