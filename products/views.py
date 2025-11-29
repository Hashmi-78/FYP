from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Category
from .forms import ProductForm


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


@login_required
def product_create_view(request):
    """
    Create a new product (seller only)
    """
    print("=" * 60)
    print("PRODUCT CREATE VIEW CALLED")
    print(f"Method: {request.method}")
    print(f"User: {request.user.username}")
    
    if request.method == 'POST':
        print("Processing POST request")
        print(f"POST data: {request.POST}")
        print(f"FILES data: {request.FILES}")
        
        form = ProductForm(request.POST, request.FILES)
        print(f"Form created: {form}")
        
        if form.is_valid():
            print("Form is valid. Creating product...")
            try:
                product = form.save(commit=False)
                product.seller = request.user
                product.save()
                
                print(f"Product created successfully: {product.name} (ID: {product.id})")
                messages.success(request, f'Product "{product.name}" created successfully!')
                return redirect('sellers:dashboard')
            except Exception as e:
                print(f"ERROR CREATING PRODUCT: {type(e).__name__}: {e}")
                import traceback
                print(f"Traceback: {traceback.format_exc()}")
                messages.error(request, f'Error creating product: {e}')
        else:
            print("FORM IS INVALID")
            print(f"Form errors: {form.errors}")
            for field, errors in form.errors.items():
                print(f"  Field '{field}': {errors}")
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        print("Processing GET request - showing empty form")
        form = ProductForm()
    
    print("Rendering product create template")
    print("=" * 60)
    
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
    print("=" * 60)
    print("PRODUCT UPDATE VIEW CALLED")
    print(f"Method: {request.method}")
    print(f"Product ID: {pk}")
    print(f"User: {request.user.username}")
    
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    print(f"Product found: {product.name}")
    
    if request.method == 'POST':
        print("Processing POST request")
        print(f"POST data: {request.POST}")
        print(f"FILES data: {request.FILES}")
        
        form = ProductForm(request.POST, request.FILES, instance=product)
        
        if form.is_valid():
            print("Form is valid. Updating product...")
            try:
                updated_product = form.save()
                print(f"Product updated successfully: {updated_product.name}")
                messages.success(request, f'Product "{updated_product.name}" updated successfully!')
                return redirect('sellers:dashboard')
            except Exception as e:
                print(f"ERROR UPDATING PRODUCT: {type(e).__name__}: {e}")
                import traceback
                print(f"Traceback: {traceback.format_exc()}")
                messages.error(request, f'Error updating product: {e}')
        else:
            print("FORM IS INVALID")
            print(f"Form errors: {form.errors}")
            for field, errors in form.errors.items():
                print(f"  Field '{field}': {errors}")
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        print("Processing GET request - showing form with existing data")
        form = ProductForm(instance=product)
    
    print("Rendering product update template")
    print("=" * 60)
    
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
    print("=" * 60)
    print("PRODUCT DELETE VIEW CALLED")
    print(f"Method: {request.method}")
    print(f"Product ID: {pk}")
    print(f"User: {request.user.username}")
    
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    print(f"Product found: {product.name}")
    
    if request.method == 'POST':
        print("Confirming deletion...")
        product_name = product.name
        try:
            product.delete()
            print(f"Product '{product_name}' deleted successfully")
            messages.success(request, f'Product "{product_name}" deleted successfully!')
        except Exception as e:
            print(f"ERROR DELETING PRODUCT: {type(e).__name__}: {e}")
            messages.error(request, f'Error deleting product: {e}')
        
        return redirect('sellers:dashboard')
    
    print("Rendering delete confirmation template")
    print("=" * 60)
    
    context = {
        'product': product,
    }
    return render(request, 'products/delete_confirm.html', context)


@login_required
def product_toggle_availability_view(request, pk):
    """
    Toggle product availability (seller only - own products)
    """
    print("=" * 60)
    print("PRODUCT TOGGLE AVAILABILITY VIEW CALLED")
    print(f"Product ID: {pk}")
    print(f"User: {request.user.username}")
    
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    print(f"Product found: {product.name}")
    print(f"Current availability: {product.is_available}")
    
    try:
        product.is_available = not product.is_available
        product.save()
        
        status = "available" if product.is_available else "unavailable"
        print(f"Product availability toggled to: {status}")
        messages.success(request, f'Product "{product.name}" is now {status}!')
    except Exception as e:
        print(f"ERROR TOGGLING AVAILABILITY: {type(e).__name__}: {e}")
        messages.error(request, f'Error updating product: {e}')
    
    print("=" * 60)
    return redirect('sellers:dashboard')
