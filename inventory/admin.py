from django.contrib import admin
from .models import Category, Part

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon_class')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')

@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'category', 'price', 'is_available')
    list_filter = ('category', 'is_available')
    search_fields = ('name', 'sku', 'description', 'specifications')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('price', 'is_available')
