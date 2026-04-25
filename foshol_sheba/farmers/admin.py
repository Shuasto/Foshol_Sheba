from django.contrib import admin
from .models import FarmerProfile

@admin.register(FarmerProfile)
class FarmerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'farm_size_in_decimals', 'created_at')
    filter_horizontal = ('primary_crops',)
    search_fields = ('user__username', 'user__phone_no')
    list_filter = ('primary_crops', 'created_at')
