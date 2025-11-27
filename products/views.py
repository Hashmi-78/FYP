from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Product, Category


def product_list_view(request):
    """
    Display list of all products with filtering and pagination
    """
    products = Product.objects.filter(is_available=True).select_related('category', 'seller')
    
    # Filter by category if provided
    category_slug = request.GET.get('category')
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    # Filter by search query
    search_query = request.GET.get('q')
    if search_query:
        products = products.filter(name__icontains=search_query)
    
    # Sorting
    sort_by = request.GET.get('sort', '-created_at')
    if sort_by in ['price', '-price', 'name', '-name', '-created_at', '-rating']:
        products = products.order_by(sort_by)
    
    # Pagination
    paginator = Paginator(products, 12)  # Show 12 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get all categories for filter
    categories = Category.objects.filter(is_active=True)
    
    context = {
        'products': page_obj,
        'categories': categories,
        'search_query': search_query,
        'current_category': category_slug,
    }
    
    return render(request, 'products/list.html', context)


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
