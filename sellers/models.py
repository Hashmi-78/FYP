from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class SellerProfile(models.Model):
    """
    Extended profile for sellers
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seller_profile')
    business_name = models.CharField(max_length=300)
    business_description = models.TextField(blank=True)
    business_logo = models.ImageField(upload_to='sellers/logos/', blank=True, null=True)
    
    # Contact information
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()
    city = models.CharField(max_length=100)

    delivery_radius = models.IntegerField(default=120, help_text="Delivery radius in km")
    
    # Business details
    tax_id = models.CharField(max_length=50, blank=True)
    bank_account = models.CharField(max_length=100, blank=True)
    
    # Ratings and stats
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    total_sales = models.IntegerField(default=0)
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    
    # Status
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.business_name


class Order(models.Model):
    """
    Order model for customer purchases
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('cod', 'Cash on Delivery'),
        ('jazzcash', 'JazzCash'),
        ('easypaisa', 'Easypaisa'),
        ('sadapay', 'SadaPay'),
        ('card', 'Credit/Debit Card'),
    ]
    
    # Order identification
    order_number = models.CharField(max_length=100, unique=True, editable=False)
    
    # Customer information
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    
    # Seller information
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller_orders')
    
    # Shipping information
    shipping_address = models.TextField()
    shipping_city = models.CharField(max_length=100)
    shipping_postal_code = models.CharField(max_length=20)
    shipping_phone = models.CharField(max_length=20)
    
    # Order details
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='cod')
    
    # Pricing
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Notes
    customer_notes = models.TextField(blank=True)
    admin_notes = models.TextField(blank=True)
    
    # Tracking
    tracking_number = models.CharField(max_length=100, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    delivered_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['order_number']),
            models.Index(fields=['customer', '-created_at']),
            models.Index(fields=['seller', '-created_at']),
            models.Index(fields=['status']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            import uuid
            self.order_number = f'ORD-{uuid.uuid4().hex[:8].upper()}'
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'Order {self.order_number} - {self.customer.username}'


class OrderItem(models.Model):
    """
    Individual items in an order
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    # Product details at time of order
    product_name = models.CharField(max_length=300)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Quantity and pricing
    quantity = models.IntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        self.subtotal = self.product_price * self.quantity
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.product_name} x {self.quantity}'


class Message(models.Model):
    """
    Messages between customers and sellers
    """
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=200)
    message = models.TextField()
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True, related_name='messages')
    
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.sender.username} → {self.recipient.username}: {self.subject}'
