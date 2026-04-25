from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'category', 'created_at')
    list_filter = ('category', 'company', 'created_at')
    search_fields = ('name', 'description', 'company__username')
    filter_horizontal = ('crops', 'target_diseases')
    readonly_fields = ('created_at', 'updated_at')
