from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from products.models import Product, Category
from .models import SellerProfile, Order
from products.forms import ProductForm


@login_required
def dashboard_view(request):
    """
    Seller dashboard with overview statistics
    """
    try:
        seller_profile = request.user.seller_profile
    except SellerProfile.DoesNotExist:
        messages.warning(request, 'Please complete your seller profile first.')
        return redirect('sellers:profile')
    
    # Get seller's products
    products_list = Product.objects.filter(seller=request.user).select_related('category')

    # Filtering
    category_slug = request.GET.get('category')
    stock_status = request.GET.get('stock')
    
    if category_slug:
        products_list = products_list.filter(category__slug=category_slug)
    
    if stock_status == 'out_of_stock':
        products_list = products_list.filter(stock=0)
    elif stock_status == 'low_stock':
        products_list = products_list.filter(stock__gt=0, stock__lte=10)
    elif stock_status == 'active':
        products_list = products_list.filter(is_available=True)
    elif stock_status == 'inactive':
        products_list = products_list.filter(is_available=False)

    # Sorting
    sort_by = request.GET.get('sort', '-created_at')
    if sort_by == 'price_asc':
        products_list = products_list.order_by('price')
    elif sort_by == 'price_desc':
        products_list = products_list.order_by('-price')
    elif sort_by == 'stock_asc':
        products_list = products_list.order_by('stock')
    elif sort_by == 'stock_desc':
        products_list = products_list.order_by('-stock')
    elif sort_by == 'date_asc':
        products_list = products_list.order_by('created_at')
    else: # date_desc or default
        products_list = products_list.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(products_list, 12) # Show 12 products per page
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    
    # Get seller's orders
    orders = Order.objects.filter(seller=request.user).order_by('-created_at')[:10]
    
    # Calculate product statistics (using base query for accurate stats)
    all_products = Product.objects.filter(seller=request.user)
    total_products = all_products.count()
    active_products = all_products.filter(is_available=True).count()
    low_stock = all_products.filter(stock__gt=0, stock__lte=10).count()  # 1-10 items
    out_of_stock = all_products.filter(stock=0).count()
    
    # Calculate order statistics
    total_orders = Order.objects.filter(seller=request.user).count()
    pending_orders = Order.objects.filter(seller=request.user, status='pending').count()
    total_revenue = seller_profile.total_revenue
    
    # Get all categories for filter dropdown
    categories = Category.objects.filter(products__seller=request.user).distinct()

    context = {
        'seller_profile': seller_profile,
        'products': products,
        'orders': orders,
        'total_products': total_products,
        'active_products': active_products,
        'low_stock': low_stock,
        'out_of_stock': out_of_stock,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'total_revenue': total_revenue,
        'categories': categories,
        'current_category': category_slug,
        'current_stock': stock_status,
        'current_sort': sort_by,
    }
    
    return render(request, 'sellers/dashboard.html', context)


@login_required
def orders_view(request):
    """
    View all seller orders
    """
    orders = Order.objects.filter(seller=request.user).order_by('-created_at')
    
    # Filter by status if provided
    status = request.GET.get('status')
    if status:
        orders = orders.filter(status=status)
    
    context = {
        'orders': orders,
        'status_choices': Order.STATUS_CHOICES,
    }
    
    return render(request, 'sellers/orders.html', context)


@login_required
def profile_view(request):
    """
    View and manage seller profile - handles both display and creation/editing
    """
    try:
        seller_profile = request.user.seller_profile
        is_new = False
    except SellerProfile.DoesNotExist:
        seller_profile = None
        is_new = True
    
    # Check if user wants to edit their profile
    show_form = is_new or request.GET.get('edit') == 'true' or request.method == 'POST'
    
    if request.method == 'POST':
        from .forms import SellerProfileForm
        
        if seller_profile:
            # Update existing profile
            form = SellerProfileForm(request.POST, request.FILES, instance=seller_profile)
        else:
            # Create new profile
            form = SellerProfileForm(request.POST, request.FILES)
        
        if form.is_valid():
            try:
                profile = form.save(commit=False)
                profile.user = request.user
                profile.save()
                
                if is_new:
                    messages.success(request, 'Seller profile created successfully! Welcome to Ahyera Store.')
                else:
                    messages.success(request, 'Profile updated successfully!')
                
                return redirect('sellers:profile')
            except Exception as e:
                messages.error(request, f'Error saving profile: {str(e)}')
        else:
            # Display form errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        from .forms import SellerProfileForm
        
        if show_form:
            # Show form for creating or editing
            if seller_profile:
                form = SellerProfileForm(instance=seller_profile)
            else:
                # Pre-fill with user's email if available
                initial_data = {'email': request.user.email} if request.user.email else {}
                form = SellerProfileForm(initial=initial_data)
        else:
            form = None
    
    context = {
        'seller_profile': seller_profile,
        'form': form,
        'is_new': is_new,
    }
    
    return render(request, 'sellers/profile.html', context)


@login_required
def add_product_view(request):
    """
    Add a new product to the seller's inventory
    """
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                product = form.save(commit=False)
                product.seller = request.user
                product.save()
                messages.success(request, f'Product "{product.name}" added successfully!')
                return redirect('sellers:dashboard')
            except Exception as e:
                messages.error(request, f'Error saving product: {str(e)}')
        else:
            # Log form errors for debugging
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = ProductForm()
    
    context = {
        'form': form,
        'title': 'Add Product'
    }
    return render(request, 'sellers/add_product.html', context)


@login_required
def edit_product_view(request, pk):
    """
    Edit an existing product
    """
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, f'Product "{product.name}" updated successfully!')
                return redirect('sellers:dashboard')
            except Exception as e:
                messages.error(request, f'Error updating product: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = ProductForm(instance=product)
    
    context = {
        'form': form,
        'product': product,
        'title': f'Edit {product.name}'
    }
    return render(request, 'sellers/add_product.html', context)


@login_required
def bulk_delete_products_view(request):
    """
    Bulk delete products
    """
    if request.method == 'POST':
        product_ids = request.POST.getlist('product_ids')
        if product_ids:
            # Filter by IDs and ensure they belong to the current user
            products_to_delete = Product.objects.filter(id__in=product_ids, seller=request.user)
            deleted_count = products_to_delete.count()
            products_to_delete.delete()
            
            if deleted_count > 0:
                messages.success(request, f'Successfully deleted {deleted_count} product(s).')
            else:
                messages.warning(request, 'No valid products found to delete.')
        else:
            messages.warning(request, 'No products selected for deletion.')
            
    return redirect('sellers:dashboard')


@login_required
def messages_view(request):
    """
    View seller messages
    """
    from .models import Message
    from django.db.models import Max
    
    # Handle sending new message
    if request.method == 'POST':
        recipient_id = request.POST.get('recipient_id')
        message_text = request.POST.get('message')
        
        if recipient_id and message_text:
            try:
                recipient = User.objects.get(id=recipient_id)
                Message.objects.create(
                    sender=request.user,
                    recipient=recipient,
                    message=message_text,
                    subject=f"Message from {request.user.username}"
                )
                messages.success(request, 'Message sent successfully!')
                return redirect(f"{request.path}?user_id={recipient_id}")
            except Exception as e:
                messages.error(request, f'Error sending message: {str(e)}')
    
    # Get all messages involving the user
    all_messages = Message.objects.filter(
        Q(sender=request.user) | Q(recipient=request.user)
    ).select_related('sender', 'recipient')
    
    # Group by conversation partner
    conversations = {}
    for msg in all_messages:
        partner = msg.recipient if msg.sender == request.user else msg.sender
        if partner.id not in conversations:
            conversations[partner.id] = {
                'partner': partner,
                'last_message': msg,
                'unread_count': 0
            }
        else:
            # Update last message if this one is newer (though query is ordered by date, better to be safe)
            if msg.created_at > conversations[partner.id]['last_message'].created_at:
                conversations[partner.id]['last_message'] = msg
        
        if msg.recipient == request.user and not msg.is_read:
            conversations[partner.id]['unread_count'] += 1
            
    # Convert to list and sort by last message date
    conversations_list = sorted(
        conversations.values(), 
        key=lambda x: x['last_message'].created_at, 
        reverse=True
    )
    
    # Get selected conversation
    selected_user_id = request.GET.get('user_id')
    selected_conversation = None
    chat_messages = []
    
    if selected_user_id:
        try:
            selected_user_id = int(selected_user_id)
            chat_messages = all_messages.filter(
                Q(sender__id=selected_user_id) | Q(recipient__id=selected_user_id)
            ).order_by('created_at')
            
            # Mark as read
            chat_messages.filter(recipient=request.user, is_read=False).update(is_read=True)
            
            selected_conversation = User.objects.get(id=selected_user_id)
        except (ValueError, User.DoesNotExist):
            pass
            
    # Total unread count
    total_unread = all_messages.filter(recipient=request.user, is_read=False).count()
    
    context = {
        'conversations': conversations_list,
        'selected_conversation': selected_conversation,
        'chat_messages': chat_messages,
        'total_unread': total_unread,
    }
    
    return render(request, 'sellers/messages.html', context)


@login_required
def delivery_view(request):
    """
    Manage delivery settings
    """
    try:
        seller_profile = request.user.seller_profile
    except SellerProfile.DoesNotExist:
        messages.warning(request, 'Please complete your seller profile first.')
        return redirect('sellers:profile')
    
    # Handle settings update
    if request.method == 'POST':
        city = request.POST.get('city')
        radius = request.POST.get('radius')
        
        if city and radius:
            try:
                seller_profile.city = city
                seller_profile.delivery_radius = int(radius)
                seller_profile.save()
                messages.success(request, 'Delivery settings updated successfully!')
            except ValueError:
                messages.error(request, 'Invalid radius value.')
            except Exception as e:
                messages.error(request, f'Error saving settings: {str(e)}')
        
        return redirect('sellers:delivery')
    
    # Get delivery statistics
    from django.db.models import Count, Q
    
    orders = Order.objects.filter(seller=request.user)
    
    delivery_stats = {
        'total_deliveries': orders.filter(status='delivered').count(),
        'in_transit': orders.filter(status='shipped').count(),
        'pending_shipment': orders.filter(status__in=['confirmed', 'processing']).count(),
        'delivery_rate': 0,
    }
    
    total_completed = orders.filter(status__in=['delivered', 'cancelled', 'refunded']).count()
    if total_completed > 0:
        delivery_stats['delivery_rate'] = (delivery_stats['total_deliveries'] / total_completed) * 100
    
    context = {
        'seller_profile': seller_profile,
        'delivery_stats': delivery_stats,
        'recent_orders': orders.filter(status='shipped')[:10],
    }
    
    return render(request, 'sellers/delivery.html', context)


@login_required
def sales_graph_view(request):
    """
    View sales analytics and graphs
    """
    from django.db.models import Sum, Count, Avg
    from django.db.models.functions import TruncDate, TruncMonth
    from datetime import datetime, timedelta
    
    # Get date range from request or default to last 30 days
    days = int(request.GET.get('days', 30))
    start_date = datetime.now() - timedelta(days=days)
    
    orders = Order.objects.filter(seller=request.user, created_at__gte=start_date)
    
    # Daily sales data
    daily_sales = orders.annotate(date=TruncDate('created_at')).values('date').annotate(
        total_sales=Sum('total'),
        order_count=Count('id')
    ).order_by('date')
    
    # Overall statistics
    stats = {
        'total_revenue': orders.aggregate(total=Sum('total'))['total'] or 0,
        'total_orders': orders.count(),
        'average_order_value': orders.aggregate(avg=Avg('total'))['avg'] or 0,
        'completed_orders': orders.filter(status='delivered').count(),
        'pending_orders': orders.filter(status='pending').count(),
    }
    
    # Top selling products
    from .models import OrderItem
    top_products = OrderItem.objects.filter(
        order__seller=request.user,
        order__created_at__gte=start_date
    ).values('product__name').annotate(
        quantity_sold=Sum('quantity'),
        revenue=Sum('subtotal')
    ).order_by('-quantity_sold')[:5]
    
    context = {
        'daily_sales': list(daily_sales),
        'stats': stats,
        'top_products': top_products,
        'days': days,
    }
    
    return render(request, 'sellers/sales_graph.html', context)


@login_required
def payment_view(request):
    """
    Manage payment and payouts
    """
    from django.db.models import Sum, Q
    
    try:
        seller_profile = request.user.seller_profile
    except SellerProfile.DoesNotExist:
        messages.warning(request, 'Please complete your seller profile first.')
        return redirect('sellers:profile')
    
    # Get payment statistics
    orders = Order.objects.filter(seller=request.user)
    
    payment_stats = {
        'total_earnings': seller_profile.total_revenue,
        'pending_payments': orders.filter(payment_status='pending').aggregate(total=Sum('total'))['total'] or 0,
        'paid_orders': orders.filter(payment_status='paid').aggregate(total=Sum('total'))['total'] or 0,
        'failed_payments': orders.filter(payment_status='failed').count(),
        'pending_count': orders.filter(payment_status='pending').count(),
    }
    
    # Recent transactions (paid orders)
    recent_transactions = orders.filter(payment_status='paid').order_by('-created_at')[:10]
    
    context = {
        'seller_profile': seller_profile,
        'payment_stats': payment_stats,
        'recent_transactions': recent_transactions,
    }
    
    return render(request, 'sellers/payment.html', context)
