from django.contrib import admin
from .models import SellerProfile, Order, OrderItem, Message


@admin.register(SellerProfile)
class SellerProfileAdmin(admin.ModelAdmin):
    list_display = ['business_name', 'user', 'city', 'rating', 'total_sales', 'is_verified', 'is_active']
    list_filter = ['is_verified', 'is_active', 'city', 'created_at']
    search_fields = ['business_name', 'user__username', 'email', 'phone']
    readonly_fields = ['rating', 'total_sales', 'total_revenue', 'created_at', 'updated_at']
    
    fieldsets = (
        ('User & Business', {
            'fields': ('user', 'business_name', 'business_description', 'business_logo')
        }),
        ('Contact Information', {
            'fields': ('phone', 'email', 'address', 'city')
        }),
        ('Business Details', {
            'fields': ('tax_id', 'bank_account')
        }),
        ('Stats & Status', {
            'fields': ('rating', 'total_sales', 'total_revenue', 'is_verified', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'customer', 'seller', 'status', 'payment_status', 'total', 'created_at']
    list_filter = ['status', 'payment_status', 'payment_method', 'created_at']
    search_fields = ['order_number', 'customer__username', 'seller__username', 'tracking_number']
    readonly_fields = ['order_number', 'created_at', 'updated_at']
    list_editable = ['status', 'payment_status']
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'customer', 'seller', 'status', 'payment_status', 'payment_method')
        }),
        ('Shipping Information', {
            'fields': ('shipping_address', 'shipping_city', 'shipping_postal_code', 'shipping_phone', 'tracking_number')
        }),
        ('Pricing', {
            'fields': ('subtotal', 'shipping_cost', 'tax', 'total')
        }),
        ('Notes', {
            'fields': ('customer_notes', 'admin_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'delivered_at')
        }),
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product_name', 'quantity', 'product_price', 'subtotal']
    list_filter = ['created_at']
    search_fields = ['order__order_number', 'product_name']
    readonly_fields = ['subtotal', 'created_at']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'recipient', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['sender__username', 'recipient__username', 'subject', 'message']
    readonly_fields = ['created_at']
