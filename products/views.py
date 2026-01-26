from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Count  # <--- Added Count here
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Category
from .forms import ProductForm

# Public View: List all products
def product_list_view(request):
    products = Product.objects.filter(is_available=True)
    
    # FIX: Annotate category with the count of AVAILABLE products only
    categories = Category.objects.annotate(
        items_count=Count('products', filter=Q(products__is_available=True))
    ).all()

    # Search
    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query)
        )

    # Category Filter
    selected_categories = request.GET.getlist('category')
    if selected_categories:
        products = products.filter(category__slug__in=selected_categories)

    # Price Range Filter
    price_range = request.GET.get('price_range')
    if price_range:
        if '-' in price_range:
            if 'plus' in price_range:
                min_price = int(price_range.split('-')[0])
                products = products.filter(price__gte=min_price)
            else:
                min_price, max_price = map(int, price_range.split('-'))
                products = products.filter(price__gte=min_price, price__lte=max_price)

    # Sorting
    sort_by = request.GET.get('sort', '-created_at')
    if sort_by == 'price':
        products = products.order_by('price')
    elif sort_by == '-price':
        products = products.order_by('-price')
    else:
        products = products.order_by('-created_at')

    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    products_data = []
    for p in page_obj:
        image_url = p.main_image.url if getattr(p, 'main_image', None) and bool(p.main_image) else ''
        price_val = float(p.get_discount_price())
        rating_val = float(p.rating or 0)

        products_data.append(
            {
                'id': p.id,
                'name': p.name,
                'price': price_val,
                'rating': rating_val,
                'image': image_url,
            }
        )

    context = {
        'products': page_obj,
        'categories': categories,
        'selected_categories': selected_categories,
        'total_count': products.count(),
        'products_data': products_data,
    }
    return render(request, 'products/list.html', context)

# ... (keep the rest of your views the same)


def product_detail_view(request, slug):
    """
    Display detailed view of a single product
    """
    product = get_object_or_404(
        Product.objects.select_related('category', 'seller'),
        slug=slug,
        is_available=True
    )
    
    # Get related products from same category
    related_products = Product.objects.filter(
        category=product.category,
        is_available=True
    ).exclude(id=product.id)[:4]
    
    # Get product reviews
    reviews = product.reviews.all().select_related('user')[:10]
    
    context = {
        'product': product,
        'related_products': related_products,
        'reviews': reviews,
    }
    
    return render(request, 'products/detail.html', context)


@login_required
def product_create_view(request):
    """
    Create a new product (seller only)
    """
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                product = form.save(commit=False)
                product.seller = request.user
                product.save()
                messages.success(request, f'Product "{product.name}" created successfully!')
                return redirect('sellers:dashboard')
            except Exception as e:
                messages.error(request, f'Error creating product: {e}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = ProductForm()
    
    context = {
        'form': form,
        'title': 'Create Product',
        'action': 'Create'
    }
    return render(request, 'products/form.html', context)


@login_required
def product_update_view(request, pk):
    """
    Update an existing product (seller only - own products)
    """
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        
        if form.is_valid():
            try:
                updated_product = form.save()
                messages.success(request, f'Product "{updated_product.name}" updated successfully!')
                return redirect('sellers:dashboard')
            except Exception as e:
                messages.error(request, f'Error updating product: {e}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = ProductForm(instance=product)
    
    context = {
        'form': form,
        'product': product,
        'title': f'Edit {product.name}',
        'action': 'Update'
    }
    return render(request, 'products/form.html', context)


@login_required
def product_delete_view(request, pk):
    """
    Delete a product (seller only - own products)
    """
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    
    if request.method == 'POST':
        product_name = product.name
        try:
            product.delete()
            messages.success(request, f'Product "{product_name}" deleted successfully!')
        except Exception as e:
            messages.error(request, f'Error deleting product: {e}')
        
        return redirect('sellers:dashboard')
    
    context = {
        'product': product,
    }
    return render(request, 'products/delete_confirm.html', context)


@login_required
def product_toggle_availability_view(request, pk):
    """
    Toggle product availability (seller only - own products)
    """
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    
    try:
        product.is_available = not product.is_available
        product.save()
        status = "available" if product.is_available else "unavailable"
        messages.success(request, f'Product "{product.name}" is now {status}!')
    except Exception as e:
        messages.error(request, f'Error updating product: {e}')

    return redirect('sellers:dashboard')
