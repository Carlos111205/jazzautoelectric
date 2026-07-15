from django.shortcuts import render
from django.db.models import Q
from .models import Category, Part

def shop(request):
    categories = Category.objects.all()
    parts = Part.objects.filter(is_available=True)
    
    # 1. Filter by category slug if provided in request
    category_slug = request.GET.get('category')
    active_category = None
    if category_slug:
        try:
            active_category = Category.objects.get(slug=category_slug)
            parts = parts.filter(category=active_category)
        except Category.DoesNotExist:
            pass
            
    # 2. Filter by search query if provided
    query = request.GET.get('q')
    if query:
        parts = parts.filter(
            Q(name__icontains=query) |
            Q(sku__icontains=query) |
            Q(description__icontains=query) |
            Q(specifications__icontains=query)
        )
        
    context = {
        'categories': categories,
        'parts': parts,
        'active_category': active_category,
        'query': query
    }
    return render(request, 'shop.html', context)
