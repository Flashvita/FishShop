from django.contrib import admin
from .models import Category, UnderCategory, Product, Order, Customer


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(UnderCategory)
class UnderCategoryAdmin(admin.ModelAdmin):
    list_display = ['title']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'under_category', 'price']
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ['category', 'under_category', 'price']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user']
